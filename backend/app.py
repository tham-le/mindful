from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import sqlite3
import pathlib
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup
DB_PATH = pathlib.Path(__file__).parent / "mindfulwealth.db"

# Global variables
preferred_currency = "EUR"  # Default currency is EUR

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
    print("Warning: google-genai package not installed. Using mock responses.")
    gemini_service = None

# Currency conversion (simplified)
def convert_currency(amount, from_currency, to_currency="EUR"):
    """Convert currency amount (simplified implementation)"""
    conversion_rates = {
        "GBP": {"EUR": 1.18},  # 1 GBP = 1.18 EUR (approximate)
        "USD": {"EUR": 0.92},  # 1 USD = 0.92 EUR (approximate)
    }
    
    if from_currency == to_currency:
        return amount
    
    if from_currency in conversion_rates and to_currency in conversion_rates[from_currency]:
        return amount * conversion_rates[from_currency][to_currency]
    
    return amount  # Default to no conversion if rate not found

# Extract currency and amount from message
def extract_currency_amount(message):
    """Extract currency and amount from message"""
    # Look for common currency patterns
    eur_pattern = r'(\d+(?:\.\d+)?)\s*(?:euros?|EUR|€)'
    gbp_pattern = r'(\d+(?:\.\d+)?)\s*(?:pounds?|GBP|£)'
    usd_pattern = r'(\d+(?:\.\d+)?)\s*(?:dollars?|USD|\$)'
    
    # Check for euros
    eur_match = re.search(eur_pattern, message, re.IGNORECASE)
    if eur_match:
        return float(eur_match.group(1)), "EUR"
    
    # Check for pounds
    gbp_match = re.search(gbp_pattern, message, re.IGNORECASE)
    if gbp_match:
        return float(gbp_match.group(1)), "GBP"
    
    # Check for dollars
    usd_match = re.search(usd_pattern, message, re.IGNORECASE)
    if usd_match:
        return float(usd_match.group(1)), "USD"
    
    # Check for plain numbers (assume EUR)
    num_pattern = r'(\d+(?:\.\d+)?)'
    num_match = re.search(num_pattern, message)
    if num_match:
        return float(num_match.group(1)), "EUR"
    
    return None, None

# Routes
@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages and return responses"""
    message = request.json.get('message', '')
    context_data = request.json.get('context_data')  # Updated field name to match frontend
    conversation_history = request.json.get('conversation_history', [])
    personality_mode = request.json.get('personality_mode', 'nice')
    
    # Set personality mode if provided
    if gemini_service and personality_mode:
        gemini_service.set_personality_mode(personality_mode)
    
    # Extract currency and amount, convert to EUR if needed
    amount, currency = extract_currency_amount(message)
    if amount is not None and currency != "EUR":
        # Convert to EUR for processing
        eur_amount = convert_currency(amount, currency)
        # Replace the original amount with the EUR amount in the message
        message = re.sub(r'\b' + str(amount) + r'\b', str(eur_amount), message)
        message = message.replace(currency, "EUR").replace("pounds", "euros").replace("£", "€")
    
    if gemini_service:
        # Use Gemini API for response with conversation history
        response = gemini_service.analyze_message(message, conversation_history, context_data)
        
        # If financial data was detected and it's a reasonable expense, add to budget
        if "financialData" in response and response["financialData"].get("type") == "reasonable":
            try:
                # Add to transactions with is_impulse=False
                financial_data = response["financialData"]
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                cursor.execute(
                    "INSERT INTO transactions (user_id, amount, category, date, description, is_impulse) VALUES (?, ?, ?, ?, ?, ?)",
                    (1, financial_data.get('amount'), financial_data.get('category'), 
                     datetime.now().isoformat(), message[:100], False)
                )
                
                # Update the budget for this category if it exists
                category = financial_data.get('category', 'Uncategorized')
                amount = financial_data.get('amount', 0)
                current_month = datetime.now().month
                current_year = datetime.now().year
                
                # Check if budget exists for this category
                cursor.execute(
                    "SELECT id, actual_amount FROM budgets WHERE user_id = ? AND category = ? AND month = ? AND year = ?",
                    (1, category, current_month, current_year)
                )
                budget_row = cursor.fetchone()
                
                if budget_row:
                    # Update existing budget
                    budget_id, current_amount = budget_row
                    new_amount = current_amount + amount
                    cursor.execute(
                        "UPDATE budgets SET actual_amount = ? WHERE id = ?",
                        (new_amount, budget_id)
                    )
                else:
                    # Create new budget entry with default planned amount
                    cursor.execute(
                        "INSERT INTO budgets (user_id, category, planned_amount, actual_amount, month, year) VALUES (?, ?, ?, ?, ?, ?)",
                        (1, category, amount * 1.2, amount, current_month, current_year)
                    )
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                print(f"Error adding to budget: {str(e)}")
                # Don't fail the whole request if budget update fails
        
        # If financial data was detected and it's an impulse purchase, add to saved impulses
        elif "financialData" in response and response["financialData"].get("type") == "impulse":
            try:
                # Add to saved impulses
                financial_data = response["financialData"]
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # Only add if it has the required fields
                if 'amount' in financial_data and 'category' in financial_data:
                    amount = financial_data.get('amount', 0)
                    category = financial_data.get('category', 'Uncategorized')
                    one_year = financial_data.get('potential_value_1yr', amount * 1.08)
                    five_year = financial_data.get('potential_value_5yr', amount * (1.08 ** 5))
                    
                    cursor.execute(
                        "INSERT INTO saved_impulses (user_id, description, amount, category, date, projected_value_1yr, projected_value_5yr) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (1, message[:100], amount, category, datetime.now().isoformat(), one_year, five_year)
                    )
                    
                    conn.commit()
                
                conn.close()
                
            except Exception as e:
                print(f"Error adding to saved impulses: {str(e)}")
                # Don't fail the whole request if saved impulses update fails
        
        return jsonify(response)
    else:
        # Use mock response for development
        return jsonify(get_mock_response(message, conversation_history, context_data))

@app.route('/api/personality', methods=['POST'])
def set_personality():
    """Set the personality mode for the chatbot"""
    mode = request.json.get('mode', 'nice')
    
    if gemini_service:
        gemini_service.set_personality_mode(mode)
        return jsonify({"success": True, "mode": mode})
    else:
        return jsonify({"success": False, "error": "Gemini service not available"})

@app.route('/api/currency', methods=['GET', 'POST'])
def set_currency():
    """Get or set the preferred currency"""
    global preferred_currency
    
    if request.method == 'POST':
        currency = request.json.get('currency', 'EUR')
        if currency in ['EUR', 'GBP', 'USD']:
            preferred_currency = currency
            if gemini_service:
                gemini_service.set_preferred_currency(currency)
            return jsonify({"success": True, "currency": currency})
        else:
            return jsonify({"success": False, "error": "Invalid currency. Supported currencies: EUR, GBP, USD"})
    else:
        return jsonify({"currency": preferred_currency})

# Update the mock response function to handle reasonable expenses
def get_mock_response(message, conversation_history=None, context_data=None):
    """Generate a mock response for development purposes
    
    Args:
        message: The user message
        conversation_history: List of previous messages
        context_data: Additional context about the conversation
        
    Returns:
        Dict with response and financial data
    """
    # Extract current context if available
    current_context = {}
    if context_data and 'currentContext' in context_data:
        current_context = context_data['currentContext']
    
    # Check if we're in an ongoing financial discussion
    ongoing_discussion = False
    last_mentioned_item = None
    last_mentioned_amount = None
    last_detected_type = None
    
    if current_context:
        ongoing_discussion = current_context.get('ongoingDiscussion', False)
        last_mentioned_item = current_context.get('lastMentionedItem')
        last_mentioned_amount = current_context.get('lastMentionedAmount')
        last_detected_type = current_context.get('lastDetectedType')
    
    # Get personality mode
    personality_mode = "nice"
    if context_data and 'conversationFlow' in context_data:
        personality_mode = context_data['conversationFlow'].get('personalityMode', 'nice')
    
    # Check for follow-up patterns in ongoing discussions
    if ongoing_discussion and last_mentioned_item and last_mentioned_amount:
        # Check if user is confirming it was an impulse purchase
        if re.search(r'impulse|moment|quick|spur|spontaneous|unplanned', message, re.I):
            if personality_mode == "sarcastic":
                return {
                    "response": f"Ah, the classic impulse buy! 🛍️ Don't worry, we've all been there - that moment when your wallet makes decisions before your brain catches up! Those {last_mentioned_amount} euros might be walking away on your {last_mentioned_item} now, but just think - that same money could have been making little euro babies in an investment account! Next time that impulse hits, maybe give me a quick chat first? I promise I'll only judge you a little bit! 😜",
                    "financialData": {
                        "type": "impulse",
                        "amount": last_mentioned_amount,
                        "category": last_mentioned_item,
                        "potential_value_1yr": round(last_mentioned_amount * 1.08, 2),
                        "potential_value_5yr": round(last_mentioned_amount * (1.08 ** 5), 2)
                    }
                }
            else:
                return {
                    "response": f"I understand. Impulse purchases happen to everyone. I've added these {last_mentioned_item} to your impulse tracker. Next time you feel the urge to make an unplanned purchase, try checking in with me first - I can help you evaluate whether it's worth it in the long run.",
                    "financialData": {
                        "type": "impulse",
                        "amount": last_mentioned_amount,
                        "category": last_mentioned_item,
                        "potential_value_1yr": round(last_mentioned_amount * 1.08, 2),
                        "potential_value_5yr": round(last_mentioned_amount * (1.08 ** 5), 2)
                    }
                }
        
        # Check if user is saying it was a planned purchase
        if re.search(r'planned|needed|necessary|essential|thought about|saving for', message, re.I):
            if personality_mode == "sarcastic":
                return {
                    "response": f"Oh, so you're telling me those {last_mentioned_item} were a carefully planned financial decision? 🤔 Well, aren't you the responsible one! I'll move this from the \"impulse buy\" category to \"totally necessary purchases.\" Your financial advisor would be so proud! 👏",
                    "financialData": {
                        "type": "reasonable",
                        "amount": last_mentioned_amount,
                        "category": last_mentioned_item,
                        "budget_allocation": True
                    }
                }
            else:
                return {
                    "response": f"That's great to hear you planned for this purchase! I've updated my records to categorize these {last_mentioned_item} as a planned expense rather than an impulse buy. Planning purchases in advance is a great financial habit.",
                    "financialData": {
                        "type": "reasonable",
                        "amount": last_mentioned_amount,
                        "category": last_mentioned_item,
                        "budget_allocation": True
                    }
                }
    
    # Check for specific patterns in the message
    # Pattern for impulse purchases
    impulse_match = re.search(r'(want|thinking|considering|looking)\s+(?:to|at|of|about)\s+(?:buy|buying|getting|purchasing)\s+(?:a|an|some)\s+([^.]+?)\s+for\s+(\d+(?:\.\d+)?)\s*(euros?|€|pounds?|£|dollars?|\$)', message, re.I)
    if impulse_match:
        item = impulse_match.group(2).strip()
        amount = float(impulse_match.group(3))
        currency = impulse_match.group(4)
        
        # Convert to EUR if needed
        if re.search(r'pounds?|£', currency, re.I):
            amount = convert_currency(amount, "GBP")
            currency = "euros"
        elif re.search(r'dollars?|\$', currency, re.I):
            amount = convert_currency(amount, "USD")
            currency = "euros"
        
        one_year = round(amount * 1.08, 2)
        five_year = round(amount * (1.08 ** 5), 2)
        
        if personality_mode == "sarcastic":
            return {
                "response": f"So you're eyeing {item} for {amount} {currency}? 🛍️ Let me put on my financial advisor hat for a second. If you invested that money instead, it could grow to {one_year} {currency} in just one year, or a whopping {five_year} {currency} in five years! But hey, who needs financial security when you have {item}, right? 😜 Is this something you've been planning to buy, or just a spur-of-the-moment desire?",
                "financialData": {
                    "type": "impulse",
                    "amount": amount,
                    "category": item,
                    "potential_value_1yr": one_year,
                    "potential_value_5yr": five_year
                }
            }
        else:
            return {
                "response": f"I see you're considering buying {item} for {amount} {currency}. If you invested this amount instead, it could grow to approximately {one_year} {currency} in one year or {five_year} {currency} in five years. Would you like me to help you evaluate if this purchase aligns with your financial goals?",
                "financialData": {
                    "type": "impulse",
                    "amount": amount,
                    "category": item,
                    "potential_value_1yr": one_year,
                    "potential_value_5yr": five_year
                }
            }
    
    # Pattern for completed purchases
    purchase_match = re.search(r'(spent|bought|purchased|paid)\s+(\d+(?:\.\d+)?)\s*(euros?|€|pounds?|£|dollars?|\$)\s+(?:on|for)\s+([^.]+)', message, re.I)
    if purchase_match:
        action = purchase_match.group(1).lower()
        amount = float(purchase_match.group(2))
        currency = purchase_match.group(3)
        item = purchase_match.group(4).strip()
        
        # Convert to EUR if needed
        if re.search(r'pounds?|£', currency, re.I):
            amount = convert_currency(amount, "GBP")
            currency = "euros"
        elif re.search(r'dollars?|\$', currency, re.I):
            amount = convert_currency(amount, "USD")
            currency = "euros"
        
        # Check if this is a reasonable expense
        reasonable_categories = ["groceries", "food", "rent", "bills", "utilities", "healthcare", "medical", "education"]
        is_reasonable = any(category in item.lower() for category in reasonable_categories)
        
        if is_reasonable:
            if personality_mode == "sarcastic":
                return {
                    "response": f"Ah, {amount} {currency} on {item}. Well, at least it's a necessary expense. I've added it to your budget, though I'm sure you could have found a better deal if you tried. 😏 Anything else you want to tell me about your spending habits?",
                    "financialData": {
                        "type": "reasonable",
                        "amount": amount,
                        "category": item,
                        "budget_allocation": True
                    }
                }
            else:
                return {
                    "response": f"I've recorded your {amount} {currency} expense for {item}. This looks like a necessary purchase, so I've added it to your monthly budget. Is there anything else you'd like me to track?",
                    "financialData": {
                        "type": "reasonable",
                        "amount": amount,
                        "category": item,
                        "budget_allocation": True
                    }
                }
        else:
            one_year = round(amount * 1.08, 2)
            five_year = round(amount * (1.08 ** 5), 2)
            
            if personality_mode == "sarcastic":
                return {
                    "response": f"So you dropped {amount} {currency} on {item}? 💸 That money could have been {one_year} {currency} in a year if invested, or {five_year} {currency} in five years! But I'm sure the {item} was totally worth it... 😏 Was this a planned purchase or did you just get caught up in the moment?",
                    "financialData": {
                        "type": "impulse",
                        "amount": amount,
                        "category": item,
                        "potential_value_1yr": one_year,
                        "potential_value_5yr": five_year
                    }
                }
            else:
                return {
                    "response": f"I see you spent {amount} {currency} on {item}. If you had invested this amount instead, it could grow to approximately {one_year} {currency} in one year or {five_year} {currency} in five years. Would you like me to add this to your impulse purchases tracker?",
                    "financialData": {
                        "type": "impulse",
                        "amount": amount,
                        "category": item,
                        "potential_value_1yr": one_year,
                        "potential_value_5yr": five_year
                    }
                }
    
    # Default response if no pattern matches
    if personality_mode == "sarcastic":
        return {
            "response": "I'm not quite sure what you're asking about. Care to share some financial decisions you're pondering? Maybe something you're thinking of buying? I promise my judgment will be only slightly cutting! 😉",
            "financialData": None
        }
    else:
        return {
            "response": "I'm here to help with your financial decisions. Feel free to tell me about any purchases you're considering or expenses you want to track.",
            "financialData": None
        }

@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
    """Handle transaction data"""
    if request.method == 'POST':
        # Add new transaction
        data = request.json
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO transactions (user_id, amount, category, date, description, is_impulse) VALUES (?, ?, ?, ?, ?, ?)",
            (1, data.get('amount'), data.get('category'), data.get('date', datetime.now().isoformat()), 
             data.get('description', ''), data.get('is_impulse', False))
        )
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'id': cursor.lastrowid})
    else:
        # Get transactions
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM transactions WHERE user_id = 1 ORDER BY date DESC")
        transactions = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify({'transactions': transactions})

@app.route('/api/budget', methods=['GET'])
def budget():
    """Return budget information"""
    # For MVP, return hardcoded data
    # In a real app, this would be fetched from the database
    return jsonify({
        'starting_balance': 230,
        'ending_balance': 1673,
        'expenses': {
            'planned': 1391,
            'actual': 944
        },
        'income': {
            'planned': 2387,
            'actual': 2387
        },
        'categories': [
            {'name': 'Food', 'planned': 120, 'actual': 22},
            {'name': 'Gifts', 'planned': 400, 'actual': 400},
            {'name': 'Home', 'planned': 470, 'actual': 470},
            {'name': 'Restaurant', 'planned': 100, 'actual': 35}
        ]
    })

@app.route('/api/saved-impulses', methods=['GET', 'POST'])
def saved_impulses():
    """Handle saved impulse purchases"""
    if request.method == 'POST':
        # Save a redirected impulse purchase
        data = request.json
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Calculate 5-year projection (if not provided)
        amount = data.get('amount', 0)
        projected_1yr = data.get('potential_value', amount * 1.08)
        projected_5yr = data.get('potential_value_5yr', amount * (1.08 ** 5))
        
        cursor.execute(
            "INSERT INTO saved_impulses (user_id, description, amount, category, date, projected_value_1yr, projected_value_5yr) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (1, data.get('item'), amount, data.get('category', 'Uncategorized'), 
             data.get('date', datetime.now().isoformat()), projected_1yr, projected_5yr)
        )
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'id': cursor.lastrowid})
    else:
        # For MVP, return hardcoded data
        # In a real app, this would be fetched from the database
        return jsonify({
            'saved_impulses': [
                {'item': 'Designer Shoes', 'amount': 150, 'potential_value': 162},
                {'item': 'Tech Gadget', 'amount': 299, 'potential_value': 323}
            ]
        })

if __name__ == '__main__':
    app.run(debug=True) 