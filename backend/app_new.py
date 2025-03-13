from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import sqlite3
import pathlib
from dotenv import load_dotenv
import re
from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker
from models import Base, User, Transaction, Budget, SavedImpulse

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup
DB_PATH = pathlib.Path(__file__).parent / "mindfulwealth.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Global variables
preferred_currency = "EUR"  # Default currency is EUR
personality_mode = "balanced"  # Default personality mode

def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    
    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        is_impulse BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create budgets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT NOT NULL,
        planned_amount REAL NOT NULL,
        actual_amount REAL NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create saved_impulses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS saved_impulses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        date TEXT NOT NULL,
        projected_value_1yr REAL NOT NULL,
        projected_value_5yr REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Insert a default user if none exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Default User",))
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Import Gemini service
try:
    from services.gemini_service import GeminiService
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        gemini_service = GeminiService(api_key)
    else:
        print("Warning: GEMINI_API_KEY environment variable not set. Using mock responses.")
        gemini_service = None
except ImportError:
    print("Warning: GeminiService not available. Using mock responses.")
    gemini_service = None

def convert_currency(amount, from_currency, to_currency="EUR"):
    """
    Convert amount from one currency to another
    For simplicity, using fixed conversion rates
    """
    # Simplified conversion rates (in real app, would use an API)
    rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "GBP": 0.75,
        "JPY": 110.0
    }
    
    # Convert to USD first (as base currency)
    amount_usd = amount / rates[from_currency]
    # Then convert to target currency
    return amount_usd * rates[to_currency]

def extract_currency_amount(message):
    """Extract currency and amount from a message"""
    # Look for currency symbols
    currency_patterns = {
        "USD": r'\$(\d+(?:\.\d+)?)',
        "EUR": r'€(\d+(?:\.\d+)?)',
        "GBP": r'£(\d+(?:\.\d+)?)',
        "JPY": r'¥(\d+(?:\.\d+)?)'
    }
    
    for currency, pattern in currency_patterns.items():
        match = re.search(pattern, message)
        if match:
            return currency, float(match.group(1))
    
    # Look for currency codes
    code_pattern = r'(\d+(?:\.\d+)?)\s*(USD|EUR|GBP|JPY)'
    match = re.search(code_pattern, message, re.IGNORECASE)
    if match:
        return match.group(2).upper(), float(match.group(1))
    
    # If no currency specified, assume it's in the preferred currency
    amount_pattern = r'(\d+(?:\.\d+)?)'
    match = re.search(amount_pattern, message)
    if match:
        return preferred_currency, float(match.group(1))
    
    return None, None

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Process chat messages and return AI responses
    """
    data = request.json
    message = data.get('message', '')
    context_data = data.get('contextData', {})
    conversation_history = data.get('conversationHistory', [])
    
    # Extract financial data if present in the message
    currency, amount = extract_currency_amount(message)
    
    # If amount is detected, convert to preferred currency if needed
    if amount is not None and currency != preferred_currency:
        converted_amount = convert_currency(amount, currency, preferred_currency)
        financial_data = {
            'original': {'amount': amount, 'currency': currency},
            'converted': {'amount': converted_amount, 'currency': preferred_currency}
        }
    elif amount is not None:
        financial_data = {
            'original': {'amount': amount, 'currency': currency},
            'converted': None  # No conversion needed
        }
    else:
        financial_data = None
    
    # Get response from AI service if available
    if gemini_service:
        try:
            # Format conversation history for the AI
            formatted_history = []
            for msg in conversation_history:
                role = "user" if msg.get('isUser') else "assistant"
                formatted_history.append({
                    "role": role,
                    "content": msg.get('text', '')
                })
            
            # Add personality context
            system_prompt = f"You are a financial advisor with a {personality_mode} approach to finances."
            
            # Get response from Gemini
            response = gemini_service.generate_response(
                message, 
                system_prompt=system_prompt,
                conversation_history=formatted_history,
                context_data=context_data
            )
            
            return jsonify({
                'response': response,
                'financial_data': financial_data
            })
        except Exception as e:
            print(f"Error with Gemini service: {str(e)}")
            # Fall back to mock response
            mock_response = get_mock_response(message, conversation_history, context_data)
            return jsonify({
                'response': mock_response,
                'financial_data': financial_data
            })
    else:
        # Use mock response if no AI service available
        mock_response = get_mock_response(message, conversation_history, context_data)
        return jsonify({
            'response': mock_response,
            'financial_data': financial_data
        })

@app.route('/api/personality', methods=['POST'])
def set_personality():
    """Set the personality mode for the financial advisor"""
    global personality_mode
    data = request.json
    mode = data.get('mode', 'balanced')
    
    # Validate mode
    valid_modes = ['conservative', 'balanced', 'aggressive']
    if mode not in valid_modes:
        return jsonify({'success': False, 'error': 'Invalid personality mode'}), 400
    
    personality_mode = mode
    return jsonify({'success': True, 'mode': personality_mode})

@app.route('/api/currency', methods=['GET', 'POST'])
def set_currency():
    """Get or set the preferred currency"""
    global preferred_currency
    
    if request.method == 'POST':
        data = request.json
        currency = data.get('currency', 'EUR')
        
        # Validate currency
        valid_currencies = ['USD', 'EUR', 'GBP', 'JPY']
        if currency not in valid_currencies:
            return jsonify({'success': False, 'error': 'Invalid currency'}), 400
        
        preferred_currency = currency
        return jsonify({'success': True, 'currency': preferred_currency})
    else:
        return jsonify({'currency': preferred_currency})

def get_mock_response(message, conversation_history=None, context_data=None):
    """Generate a mock response for development when AI service is unavailable"""
    message_lower = message.lower()
    
    # Basic responses based on message content
    if 'hello' in message_lower or 'hi' in message_lower:
        return "Hello! I'm your financial advisor. How can I help you today?"
    
    if 'budget' in message_lower:
        return "Based on your current spending patterns, I recommend allocating 50% of your income to necessities, 30% to wants, and 20% to savings and debt repayment."
    
    if 'save' in message_lower or 'saving' in message_lower:
        return "Saving money is crucial for financial security. I recommend setting up automatic transfers to a high-yield savings account right after each payday."
    
    if 'invest' in message_lower or 'investment' in message_lower:
        if personality_mode == 'conservative':
            return "For a conservative approach, consider a portfolio with 60% bonds and 40% stocks, focusing on blue-chip companies with stable dividends."
        elif personality_mode == 'aggressive':
            return "With an aggressive investment strategy, you might want to allocate 80% to stocks, including growth stocks and emerging markets, and 20% to bonds."
        else:  # balanced
            return "A balanced portfolio typically consists of 60% stocks and 40% bonds, providing a good mix of growth potential and stability."
    
    if 'impulse' in message_lower or 'purchase' in message_lower:
        return "Before making an impulse purchase, consider waiting 24 hours. If you still want it after that time, evaluate if it fits within your budget and aligns with your financial goals."
    
    if 'debt' in message_lower:
        return "To tackle debt effectively, consider the avalanche method (paying off highest interest debt first) or the snowball method (paying off smallest debts first for psychological wins)."
    
    if 'retirement' in message_lower:
        return "For retirement planning, aim to save at least 15% of your income. Take advantage of employer matches in retirement accounts, and consider diversifying with a mix of pre-tax and Roth contributions."
    
    # Default response
    return "That's an interesting question about your finances. To give you the best advice, I'd need to understand more about your financial situation, goals, and risk tolerance."

@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
    """Get or add transactions"""
    session = Session()
    
    try:
        if request.method == 'POST':
            # Add a new transaction
            data = request.json
            
            # Validate required fields
            required_fields = ['amount', 'category', 'date', 'description']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
            
            # Create new transaction
            new_transaction = Transaction(
                user_id=1,  # Default user
                amount=data['amount'],
                category=data['category'],
                date=datetime.fromisoformat(data['date']) if isinstance(data['date'], str) else datetime.now(),
                description=data['description'],
                is_impulse=data.get('is_impulse', False)
            )
            
            session.add(new_transaction)
            session.commit()
            
            return jsonify({
                'success': True,
                'id': new_transaction.id,
                'transaction': new_transaction.to_dict()
            })
        else:
            # Get all transactions
            transactions = session.query(Transaction).filter_by(user_id=1).all()
            return jsonify([t.to_dict() for t in transactions])
    
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        session.close()

@app.route('/api/budget', methods=['GET', 'POST'])
def budget():
    """Get or update budget information"""
    session = Session()
    
    try:
        if request.method == 'POST':
            # Update budget
            data = request.json
            
            # Validate required fields
            required_fields = ['category', 'planned_amount', 'month', 'year']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
            
            # Check if budget already exists for this category/month/year
            existing_budget = session.query(Budget).filter_by(
                user_id=1,
                category=data['category'],
                month=data['month'],
                year=data['year']
            ).first()
            
            if existing_budget:
                # Update existing budget
                existing_budget.planned_amount = data['planned_amount']
                session.commit()
                return jsonify({'success': True, 'budget': existing_budget.to_dict()})
            else:
                # Create new budget
                new_budget = Budget(
                    user_id=1,
                    category=data['category'],
                    planned_amount=data['planned_amount'],
                    actual_amount=0,  # Initialize with zero
                    month=data['month'],
                    year=data['year']
                )
                session.add(new_budget)
                session.commit()
                return jsonify({'success': True, 'budget': new_budget.to_dict()})
        else:
            # Get current month's budget
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Get budget items for current month
            budgets = session.query(Budget).filter_by(
                user_id=1,
                month=current_month,
                year=current_year
            ).all()
            
            # Calculate total budget and spent
            total_planned = sum(b.planned_amount for b in budgets)
            total_actual = sum(b.actual_amount for b in budgets)
            
            # Get spending by category
            categories = []
            for budget in budgets:
                categories.append({
                    'name': budget.category,
                    'planned': budget.planned_amount,
                    'actual': budget.actual_amount
                })
            
            return jsonify({
                'total': total_planned,
                'spent': total_actual,
                'categories': categories
            })
    
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        session.close()

@app.route('/api/saved-impulses', methods=['GET', 'POST'])
def saved_impulses():
    """Get or add saved impulse purchases"""
    session = Session()
    
    try:
        if request.method == 'POST':
            # Add a new saved impulse
            data = request.json
            
            # Validate required fields
            required_fields = ['description', 'amount', 'category']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
            
            # Calculate projected values (simple calculation for demo)
            amount = float(data['amount'])
            projected_1yr = amount * 1.07  # 7% annual return
            projected_5yr = amount * (1.07 ** 5)  # Compound over 5 years
            
            # Create new saved impulse
            new_impulse = SavedImpulse(
                user_id=1,  # Default user
                description=data['description'],
                amount=amount,
                category=data['category'],
                date=datetime.now(),
                projected_value_1yr=projected_1yr,
                projected_value_5yr=projected_5yr
            )
            
            session.add(new_impulse)
            session.commit()
            
            return jsonify({
                'success': True,
                'id': new_impulse.id,
                'impulse': new_impulse.to_dict()
            })
        else:
            # Get all saved impulses
            impulses = session.query(SavedImpulse).filter_by(user_id=1).all()
            return jsonify([i.to_dict() for i in impulses])
    
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        session.close()

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Get dashboard data"""
    session = Session()
    
    try:
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Get transactions for current month
        transactions = session.query(Transaction).filter(
            Transaction.user_id == 1,
            extract('month', Transaction.date) == current_month,
            extract('year', Transaction.date) == current_year
        ).all()
        
        # Get budget for current month
        budgets = session.query(Budget).filter_by(
            user_id=1,
            month=current_month,
            year=current_year
        ).all()
        
        # Get saved impulses
        impulses = session.query(SavedImpulse).filter_by(user_id=1).all()
        
        # Calculate total spent this month
        total_spent = sum(t.amount for t in transactions)
        
        # Calculate total budget
        total_budget = sum(b.planned_amount for b in budgets)
        
        # Calculate total saved from impulses
        total_saved = sum(i.amount for i in impulses)
        
        # Calculate potential growth
        potential_growth_1yr = sum(i.projected_value_1yr for i in impulses)
        
        # Group transactions by category
        spending_by_category = {}
        for transaction in transactions:
            category = transaction.category
            if category not in spending_by_category:
                spending_by_category[category] = 0
            spending_by_category[category] += transaction.amount
        
        # Format for frontend
        categories = []
        for category, amount in spending_by_category.items():
            # Find budget for this category if it exists
            budget_item = next((b for b in budgets if b.category == category), None)
            planned = budget_item.planned_amount if budget_item else 0
            
            categories.append({
                'name': category,
                'spent': amount,
                'budget': planned
            })
        
        # Recent transactions (last 5)
        recent_transactions = sorted(transactions, key=lambda t: t.date, reverse=True)[:5]
        
        return jsonify({
            'total_spent': total_spent,
            'total_budget': total_budget,
            'total_saved': total_saved,
            'potential_growth': potential_growth_1yr,
            'categories': categories,
            'recent_transactions': [t.to_dict() for t in recent_transactions],
            'saved_impulses': [i.to_dict() for i in impulses][:5]  # Last 5 saved impulses
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 