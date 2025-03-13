import sys
import os

# Add the site-packages directory to the Python path
site_packages_path = os.path.join(os.path.expanduser("~"), "env/lib/python3.12/site-packages")
if os.path.exists(site_packages_path) and site_packages_path not in sys.path:
    sys.path.append(site_packages_path)

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
    import json
    from datetime import datetime, timedelta
    import sqlite3
    import pathlib
    from dotenv import load_dotenv
    import re
    from sqlalchemy import create_engine, extract
    from sqlalchemy.orm import sessionmaker
    from models import Base, User, Transaction, Budget, SavedImpulse
    from routes.auth_routes import auth_bp, setup_auth_routes
    from services.gemini_service import GeminiService, GENAI_AVAILABLE
    import logging
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes with support for credentials
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Database setup
DB_PATH = pathlib.Path(__file__).parent / "mindfulwealth.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

# Global variables
preferred_currency = "EUR"  # Default currency is EUR
personality_mode = "nice"  # Default personality mode is now 'nice'

# Category translations
category_translations = {
    'fr': {
        'savings': 'épargne',
        'groceries': 'courses',
        'food': 'alimentation',
        'rent': 'loyer',
        'mortgage': 'hypothèque',
        'utilities': 'services publics',
        'transportation': 'transport',
        'healthcare': 'santé',
        'insurance': 'assurance',
        'entertainment': 'divertissement',
        'clothing': 'vêtements',
        'education': 'éducation',
        'travel': 'voyage',
        'dining': 'restauration',
        'electronics': 'électronique',
        'home': 'maison',
        'general': 'général',
        'childcare': 'garde d\'enfants',
        'gifts': 'cadeaux',
        'personal': 'personnel',
        'debt': 'dette',
        'investment': 'investissement',
        'subscription': 'abonnement',
        'charity': 'charité',
        'taxes': 'impôts',
        'other': 'autre'
    }
}

# Helper function to translate categories
def translate_category(category, language='fr'):
    """Translate a category name to the specified language"""
    if language == 'en' or language not in category_translations:
        return category
        
    category_lower = category.lower()
    translations = category_translations[language]
    
    if category_lower in translations:
        return translations[category_lower]
        
    # Try to find partial matches
    for eng_cat, translated_cat in translations.items():
        if eng_cat in category_lower or category_lower in eng_cat:
            return translated_cat
            
    # Return original if no translation found
    return category

# Initialize Gemini service if available
gemini_service = None
gemini_api_key = os.getenv('GEMINI_API_KEY')
if GENAI_AVAILABLE and gemini_api_key:
    try:
        gemini_service = GeminiService(gemini_api_key)
        gemini_service.set_personality_mode(personality_mode)
        gemini_service.set_preferred_currency(preferred_currency)
        print("Gemini service initialized successfully.")
    except Exception as e:
        print(f"Error initializing Gemini service: {str(e)}")
        print("Using mock responses instead.")
else:
    print("Gemini service disabled. Using mock responses.")

# Register auth routes
auth_routes = setup_auth_routes(db_session)
app.register_blueprint(auth_routes, url_prefix='/api/auth')

# Helper function to get current user
def get_current_user():
    """Get the current authenticated user"""
    try:
        user_id = get_jwt_identity()
        return db_session.query(User).filter(User.id == user_id).first()
    except:
        return None

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
@jwt_required(optional=True)
def chat():
    """
    Process chat messages and return AI responses
    """
    data = request.json
    
    # Get current user if authenticated
    current_user = get_current_user()
    user_id = current_user.id if current_user else None
    
    # Get user's language preference
    language_preference = current_user.language_preference if current_user else 'fr'
    
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
    
    # Use Gemini service if available
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
            
            # Add personality context and language preference
            system_prompt = f"You are a financial advisor with a {personality_mode} approach to finances. Please respond in {language_preference} language."
            
            # Get response from Gemini
            response = gemini_service.get_response(
                message, 
                system_prompt=system_prompt,
                conversation_history=formatted_history,
                context_data=context_data,
                language=language_preference
            )
            
            return jsonify({
                'response': response,
                'financial_data': financial_data
            })
        except Exception as e:
            print(f"Error with Gemini service: {str(e)}")
            # Fall back to mock response
            mock_response = get_mock_response(message, conversation_history, context_data, language_preference)
            return jsonify({
                'response': mock_response,
                'financial_data': financial_data
            })
    else:
        # Use mock response if no AI service available
        mock_response = get_mock_response(message, conversation_history, context_data, language_preference)
        return jsonify({
            'response': mock_response,
            'financial_data': financial_data
        })

@app.route('/api/personality', methods=['POST'])
@jwt_required(optional=True)
def set_personality():
    """Set the personality mode for the chatbot"""
    try:
        # Get the personality mode from the request
        data = request.get_json()
        if not data or 'mode' not in data:
            return jsonify({'error': 'Missing personality mode'}), 400
            
        mode = data['mode']
        if mode not in ['nice', 'funny', 'irony']:
            return jsonify({'error': f'Invalid personality mode: {mode}'}), 400
        
        # Set the global personality mode
        global personality_mode
        personality_mode = mode
        
        # Set the personality mode in the Gemini service if available
        if gemini_service:
            gemini_service.set_personality_mode(mode)
            logger.info(f"Personality mode set to: {mode} in Gemini service")
        
        # Get the current user if authenticated
        current_user = get_current_user()
        
        # If user is authenticated, update their preference in the database
        if current_user:
            try:
                # Create a new session for this operation
                session = Session()
                
                # Update the user's personality preference
                user = session.query(User).filter(User.id == current_user.id).first()
                if user:
                    user.personality_preference = mode
                    session.commit()
                    logger.info(f"Updated personality preference for user {user.id} to {mode}")
                
                session.close()
            except Exception as e:
                logger.error(f"Error updating personality preference: {str(e)}")
                # Continue even if database update fails
        
        return jsonify({
            'success': True,
            'mode': mode
        })
    except Exception as e:
        logger.error(f"Error setting personality mode: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
        
        # Update Gemini service if available
        if gemini_service:
            gemini_service.set_preferred_currency(currency)
        
        return jsonify({'success': True, 'currency': preferred_currency})
    else:
        return jsonify({'currency': preferred_currency})

def get_mock_response(message, conversation_history=None, context_data=None, language='fr'):
    """Generate a mock response for development when AI service is unavailable"""
    message_lower = message.lower()
    
    # Extract category if present in the message
    category_pattern = r'for\s+(\w+)'
    category_match = re.search(category_pattern, message_lower)
    category = category_match.group(1) if category_match else None
    
    # If category is found, translate it
    if category and language == 'fr':
        translated_category = translate_category(category, language)
        # Replace the category in the message for processing
        message_lower = message_lower.replace(f"for {category}", f"for {translated_category}")
    
    # Basic responses based on message content, personality, and language
    if 'hello' in message_lower or 'hi' in message_lower or 'bonjour' in message_lower or 'salut' in message_lower:
        if language == 'fr':
            if personality_mode == 'nice':
                return "Bonjour ! Je suis votre conseiller financier amical. Comment puis-je vous aider aujourd'hui ?"
            elif personality_mode == 'funny':
                return "Salut ! Je suis votre conseiller financier, ici pour rendre les questions d'argent moins ennuyeuses et plus... eh bien, monétaires ! Qu'avez-vous en tête aujourd'hui ?"
            elif personality_mode == 'irony':
                return "Oh, encore une personne qui veut des conseils financiers. Laissez-moi deviner, vous voulez savoir comment devenir millionnaire du jour au lendemain ? Je suis tout ouïe."
        else:  # English
            if personality_mode == 'nice':
                return "Hello! I'm your friendly financial advisor. How can I help you today?"
            elif personality_mode == 'funny':
                return "Hey there! I'm your financial advisor, here to make money matters less boring and more... well, money-ey! What's on your financial mind today?"
            elif personality_mode == 'irony':
                return "Oh look, another person wanting financial advice. Let me guess, you want to know how to become a millionaire overnight? I'm all ears."
    
    if 'budget' in message_lower:
        if language == 'fr':
            if personality_mode == 'nice':
                return "D'après vos habitudes de dépenses actuelles, je vous recommande d'allouer 50% de vos revenus aux nécessités, 30% aux envies et 20% à l'épargne et au remboursement de dettes. Cette approche équilibrée vous aidera à atteindre vos objectifs financiers tout en profitant de la vie !"
            elif personality_mode == 'funny':
                return "Ah, le budget ! L'art de dire à votre argent où aller au lieu de vous demander où il est passé ! Je suggère la règle 50/30/20 : 50% pour les besoins, 30% pour les envies et 20% pour l'épargne. Ou comme je l'appelle : le 'sandwich adulte' - du pain responsable avec une garniture amusante !"
            elif personality_mode == 'irony':
                return "Le budget, parce qu'apparemment l'argent ne pousse pas sur les arbres. Concept révolutionnaire, je sais. Essayez l'approche 50/30/20 : 50% sur les nécessités, 30% sur les choses que vous voulez, et 20% sur l'épargne. Ou continuez simplement à dépenser au hasard et faites semblant d'être surpris quand votre compte atteint zéro. C'est votre choix."
        else:  # English
            if personality_mode == 'nice':
                return "Based on your current spending patterns, I recommend allocating 50% of your income to necessities, 30% to wants, and 20% to savings and debt repayment. This balanced approach will help you achieve your financial goals while still enjoying life!"
            elif personality_mode == 'funny':
                return "Ah, budgeting! The art of telling your money where to go instead of wondering where it went! I suggest the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. Or as I call it: the 'adulting sandwich' - responsible bread with a fun filling!"
            elif personality_mode == 'irony':
                return "Budgeting, because apparently money doesn't grow on trees. Revolutionary concept, I know. Try the 50/30/20 approach: 50% on necessities, 30% on things you want, and 20% on savings. Or just keep spending randomly and act surprised when your account hits zero. Your choice."
    
    if 'save' in message_lower or 'saving' in message_lower or 'économiser' in message_lower or 'épargne' in message_lower:
        if language == 'fr':
            if personality_mode == 'nice':
                return "Économiser de l'argent est crucial pour la sécurité financière. Je vous recommande de mettre en place des virements automatiques vers un compte d'épargne à haut rendement juste après chaque jour de paie. De cette façon, vous constituerez votre épargne de manière constante sans avoir à y penser !"
            elif personality_mode == 'funny':
                return "Économiser de l'argent, c'est comme essayer de ne pas manger le dernier biscuit du pot - difficile mais gratifiant ! Mettez en place des virements automatiques vers votre compte d'épargne le jour de paie. C'est comme si votre ancien vous rendait service à votre futur vous. Votre ancien vous est un si bon ami !"
            elif personality_mode == 'irony':
                return "Économiser de l'argent, quel concept novateur. Au lieu d'acheter des choses dont vous n'avez pas besoin avec de l'argent que vous n'avez pas pour impressionner des gens que vous n'aimez pas, vous pourriez essayer des virements automatiques vers un compte d'épargne. Révolutionnaire, je sais."
        else:  # English
            if personality_mode == 'nice':
                return "Saving money is crucial for financial security. I recommend setting up automatic transfers to a high-yield savings account right after each payday. This way, you'll build your savings consistently without having to think about it!"
            elif personality_mode == 'funny':
                return "Saving money is like trying not to eat the last cookie in the jar - difficult but rewarding! Set up automatic transfers to your savings account on payday. It's like your past self doing a favor for your future self. Past you is such a good friend!"
            elif personality_mode == 'irony':
                return "Saving money, what a novel concept. Instead of buying things you don't need with money you don't have to impress people you don't like, you could try automatic transfers to a savings account. Revolutionary, I know."
    
    # Default responses based on personality and language
    if language == 'fr':
        if personality_mode == 'nice':
            return "C'est une question financière intéressante. Pour vous donner les meilleurs conseils, j'aurais besoin de comprendre davantage votre situation et vos objectifs spécifiques. Pourriez-vous fournir plus de détails sur votre situation financière ?"
        elif personality_mode == 'funny':
            return "Hmm, c'est une énigme financière ! J'aimerais vous aider, mais j'ai besoin d'un peu plus d'informations - ma boule de cristal est en réparation ! Pourriez-vous partager plus de détails sur votre situation financière ? Plus vous me donnez de détails, moins je dois compter sur mes capacités douteuses de lecture de pensée !"
        elif personality_mode == 'irony':
            return "Eh bien, c'est vague. J'adorerais vous donner des conseils financiers personnalisés basés sur pratiquement aucune information, mais mes pouvoirs psychiques sont un peu rouillés aujourd'hui. Souhaitez-vous partager des détails réels sur votre situation ? Juste une idée."
    else:  # English
        if personality_mode == 'nice':
            return "That's an interesting financial question. To give you the best advice, I'd need to understand more about your specific situation and goals. Could you provide more details about your financial circumstances?"
        elif personality_mode == 'funny':
            return "Hmm, that's a financial head-scratcher! I'd love to help, but I need a bit more info - my crystal ball is in the shop for repairs! Could you share more about your money situation? The more details, the less I have to rely on my questionable mind-reading abilities!"
        elif personality_mode == 'irony':
            return "Well, that's vague. I'd love to give you personalized financial advice based on practically no information, but my psychic powers are a bit rusty today. Care to share some actual details about your situation? Just a thought."

@app.route('/api/transactions', methods=['GET', 'POST'])
@jwt_required()
def transactions():
    """
    Handle transaction operations
    """
    current_user = get_current_user()
    
    if request.method == 'GET':
        # Get transactions for the current user
        user_transactions = db_session.query(Transaction).filter(
            Transaction.user_id == current_user.id
        ).all()
        return jsonify([t.to_dict() for t in user_transactions])
    
    elif request.method == 'POST':
        data = request.json
        
        # Create new transaction for the current user
        transaction = Transaction(
            user_id=current_user.id,
            amount=data.get('amount'),
            category=data.get('category'),
            description=data.get('description'),
            is_impulse=data.get('is_impulse', False)
        )
        
        if 'date' in data:
            transaction.date = datetime.fromisoformat(data['date'])
        
        db_session.add(transaction)
        db_session.commit()
        
        return jsonify({'success': True, 'id': transaction.id})

@app.route('/api/budget', methods=['GET', 'POST'])
@jwt_required()
def budget():
    """
    Handle budget operations
    """
    current_user = get_current_user()
    
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
            existing_budget = db_session.query(Budget).filter_by(
                user_id=current_user.id,
                category=data['category'],
                month=data['month'],
                year=data['year']
            ).first()
            
            if existing_budget:
                # Update existing budget
                existing_budget.planned_amount = data['planned_amount']
                db_session.commit()
                return jsonify({'success': True, 'budget': existing_budget.to_dict()})
            else:
                # Create new budget
                new_budget = Budget(
                    user_id=current_user.id,
                    category=data['category'],
                    planned_amount=data['planned_amount'],
                    actual_amount=0,  # Initialize with zero
                    month=data['month'],
                    year=data['year']
                )
                db_session.add(new_budget)
                db_session.commit()
                return jsonify({'success': True, 'budget': new_budget.to_dict()})
        else:
            # Get current month's budget
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Get budget items for current month
            budgets = db_session.query(Budget).filter_by(
                user_id=current_user.id,
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
        db_session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/saved-impulses', methods=['GET', 'POST'])
@jwt_required()
def saved_impulses():
    """
    Handle saved impulse operations
    """
    current_user = get_current_user()
    
    try:
        if request.method == 'POST':
            # Add a new saved impulse
            data = request.json
            
            # Handle field name discrepancies between frontend and backend
            description = data.get('description', data.get('item', ''))
            amount = float(data.get('amount', 0))
            category = data.get('category', '')
            
            # Validate required fields
            if not description:
                return jsonify({'success': False, 'error': 'Missing required field: description/item'}), 400
            if not amount:
                return jsonify({'success': False, 'error': 'Missing required field: amount'}), 400
            if not category:
                return jsonify({'success': False, 'error': 'Missing required field: category'}), 400
            
            # Calculate projected values (simple calculation for demo)
            projected_1yr = data.get('projected_value_1yr', data.get('potential_value', amount * 1.07))  # 7% annual return
            projected_5yr = data.get('projected_value_5yr', amount * (1.07 ** 5))  # Compound over 5 years
            
            # Create new saved impulse
            new_impulse = SavedImpulse(
                user_id=current_user.id,
                description=description,
                amount=amount,
                category=category,
                date=datetime.now(),
                projected_value_1yr=projected_1yr,
                projected_value_5yr=projected_5yr
            )
            
            db_session.add(new_impulse)
            db_session.commit()
            
            return jsonify({
                'success': True,
                'id': new_impulse.id,
                'impulse': new_impulse.to_dict()
            })
        else:
            # Get all saved impulses
            impulses = db_session.query(SavedImpulse).filter_by(user_id=current_user.id).all()
            return jsonify([i.to_dict() for i in impulses])
    
    except Exception as e:
        db_session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """
    Get comprehensive dashboard data for the current user
    Includes budget tracking, spending analysis, investment projections,
    and impulse purchase redirection metrics
    """
    current_user = get_current_user()
    
    try:
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Get transactions for current month
        current_transactions = db_session.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            extract('month', Transaction.date) == current_month,
            extract('year', Transaction.date) == current_year
        ).all()
        
        # Get transactions for previous month for comparison
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        prev_transactions = db_session.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            extract('month', Transaction.date) == prev_month,
            extract('year', Transaction.date) == prev_year
        ).all()
        
        # Get all transactions for trend analysis (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        all_transactions = db_session.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= six_months_ago
        ).order_by(Transaction.date).all()
        
        # Get budget for current month
        budgets = db_session.query(Budget).filter_by(
            user_id=current_user.id,
            month=current_month,
            year=current_year
        ).all()
        
        # Get saved impulses
        impulses = db_session.query(SavedImpulse).filter_by(user_id=current_user.id).all()
        
        # Calculate total spent this month
        total_spent = sum(t.amount for t in current_transactions)
        
        # Calculate total spent last month for comparison
        prev_total_spent = sum(t.amount for t in prev_transactions)
        
        # Calculate spending change percentage
        spending_change_pct = 0
        if prev_total_spent > 0:
            spending_change_pct = round(((total_spent - prev_total_spent) / prev_total_spent) * 100, 1)
        
        # Calculate total budget
        total_budget = sum(b.planned_amount for b in budgets)
        
        # Calculate budget remaining
        budget_remaining = total_budget - total_spent
        budget_remaining_pct = 0
        if total_budget > 0:
            budget_remaining_pct = round((budget_remaining / total_budget) * 100, 1)
        
        # Calculate total saved from impulses
        total_saved = sum(i.amount for i in impulses)
        
        # Calculate potential growth
        potential_growth_1yr = sum(i.projected_value_1yr for i in impulses)
        potential_growth_5yr = sum(i.projected_value_5yr for i in impulses)
        
        # Calculate investment growth
        investment_growth_1yr = round(total_saved * 0.08, 2)
        investment_growth_5yr = round(total_saved * (1.08 ** 5 - 1), 2)
        
        # Group transactions by category
        spending_by_category = {}
        for transaction in current_transactions:
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
            
            # Calculate percentage of budget used
            budget_used_pct = 0
            if planned > 0:
                budget_used_pct = round((amount / planned) * 100, 1)
            
            categories.append({
                'name': category,
                'spent': amount,
                'budget': planned,
                'remaining': max(0, planned - amount),
                'percentage': budget_used_pct,
                'status': 'over' if amount > planned and planned > 0 else 'under'
            })
        
        # Sort categories by spending amount (descending)
        categories.sort(key=lambda x: x['spent'], reverse=True)
        
        # Generate monthly spending trend (last 6 months)
        monthly_trends = {}
        for transaction in all_transactions:
            month_key = f"{transaction.date.year}-{transaction.date.month:02d}"
            if month_key not in monthly_trends:
                monthly_trends[month_key] = {
                    'month': transaction.date.strftime('%b %Y'),
                    'total': 0,
                    'categories': {}
                }
            
            monthly_trends[month_key]['total'] += transaction.amount
            
            # Track spending by category
            category = transaction.category
            if category not in monthly_trends[month_key]['categories']:
                monthly_trends[month_key]['categories'][category] = 0
            monthly_trends[month_key]['categories'][category] += transaction.amount
        
        # Convert to list and sort by date
        trend_data = list(monthly_trends.values())
        
        # Count impulse vs. reasonable transactions
        impulse_count = len([t for t in current_transactions if t.is_impulse])
        reasonable_count = len(current_transactions) - impulse_count
        
        # Calculate impulse spending percentage
        impulse_spending = sum(t.amount for t in current_transactions if t.is_impulse)
        impulse_spending_pct = 0
        if total_spent > 0:
            impulse_spending_pct = round((impulse_spending / total_spent) * 100, 1)
        
        # Recent transactions (last 5)
        recent_transactions = sorted(current_transactions, key=lambda t: t.date, reverse=True)[:5]
        
        # Recent saved impulses (last 5)
        recent_impulses = sorted(impulses, key=lambda i: i.date, reverse=True)[:5]
        
        # Financial health indicators
        financial_health = {
            'budget_adherence': 'good' if total_spent <= total_budget else 'warning',
            'impulse_control': 'good' if impulse_spending_pct < 20 else ('warning' if impulse_spending_pct < 40 else 'poor'),
            'savings_rate': 'good' if total_saved > 0 else 'warning',
            'budget_coverage': 'good' if len(categories) > 0 and all(c['budget'] > 0 for c in categories) else 'warning'
        }
        
        # Recommendations based on spending patterns
        recommendations = []
        
        # Check for over-budget categories
        over_budget_categories = [c for c in categories if c['status'] == 'over']
        if over_budget_categories:
            top_over = over_budget_categories[0]['name']
            recommendations.append(f"Your {top_over} spending is over budget. Consider adjusting your budget or reducing spending in this category.")
        
        # Check for high impulse spending
        if impulse_spending_pct > 30:
            recommendations.append(f"Your impulse spending is {impulse_spending_pct}% of your total spending. Try using the 24-hour rule before making non-essential purchases.")
        
        # Check for missing budget categories
        missing_budget = [c['name'] for c in categories if c['budget'] == 0]
        if missing_budget:
            recommendations.append(f"Consider setting a budget for these categories: {', '.join(missing_budget[:3])}.")
        
        # Check for potential savings
        if total_saved < 100:
            recommendations.append("Try redirecting more impulse purchases to savings to build your investment portfolio.")
        
        return jsonify({
            'summary': {
                'total_spent': total_spent,
                'total_budget': total_budget,
                'budget_remaining': budget_remaining,
                'budget_remaining_pct': budget_remaining_pct,
                'spending_change_pct': spending_change_pct,
                'total_saved': total_saved,
                'potential_growth_1yr': potential_growth_1yr,
                'potential_growth_5yr': potential_growth_5yr,
                'investment_growth_1yr': investment_growth_1yr,
                'investment_growth_5yr': investment_growth_5yr,
                'impulse_spending_pct': impulse_spending_pct
            },
            'categories': categories,
            'trends': trend_data,
            'transaction_counts': {
                'impulse': impulse_count,
                'reasonable': reasonable_count,
                'total': len(current_transactions)
            },
            'financial_health': financial_health,
            'recommendations': recommendations,
            'recent_transactions': [t.to_dict() for t in recent_transactions],
            'recent_impulses': [i.to_dict() for i in recent_impulses]
        })
    
    except Exception as e:
        logger.error(f"Error generating dashboard data: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/impulses', methods=['POST'])
@jwt_required()
def save_impulse():
    """
    Save an impulse purchase that has been redirected to investment
    """
    current_user = get_current_user()
    data = request.get_json()
    
    try:
        # Validate required fields
        required_fields = ['description', 'category', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Create new saved impulse
        impulse = SavedImpulse(
            user_id=current_user.id,
            description=data['description'],
            category=data['category'],
            amount=float(data['amount']),
            notes=data.get('notes')
        )
        
        db_session.add(impulse)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Impulse purchase saved successfully',
            'impulse': impulse.to_dict()
        })
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error saving impulse purchase: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/impulses', methods=['GET'])
@jwt_required()
def get_impulses():
    """
    Get all saved impulse purchases for the current user
    """
    current_user = get_current_user()
    
    try:
        impulses = db_session.query(SavedImpulse).filter_by(user_id=current_user.id).order_by(SavedImpulse.date.desc()).all()
        
        # Calculate totals
        total_saved = sum(i.amount for i in impulses)
        total_growth_1yr = sum(i.projected_value_1yr for i in impulses) - total_saved
        total_growth_5yr = sum(i.projected_value_5yr for i in impulses) - total_saved
        
        return jsonify({
            'success': True,
            'impulses': [i.to_dict() for i in impulses],
            'summary': {
                'count': len(impulses),
                'total_saved': total_saved,
                'total_growth_1yr': total_growth_1yr,
                'total_growth_5yr': total_growth_5yr
            }
        })
    
    except Exception as e:
        logger.error(f"Error retrieving impulse purchases: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/impulses/<int:impulse_id>', methods=['DELETE'])
@jwt_required()
def delete_impulse(impulse_id):
    """
    Delete a saved impulse purchase
    """
    current_user = get_current_user()
    
    try:
        impulse = db_session.query(SavedImpulse).filter_by(id=impulse_id, user_id=current_user.id).first()
        
        if not impulse:
            return jsonify({'success': False, 'error': 'Impulse purchase not found'}), 404
        
        db_session.delete(impulse)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Impulse purchase deleted successfully'
        })
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error deleting impulse purchase: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/transactions', methods=['POST'])
@jwt_required()
def add_transaction():
    """
    Add a new transaction for the current user
    """
    current_user = get_current_user()
    data = request.get_json()
    
    try:
        # Validate required fields
        required_fields = ['amount', 'category', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Parse date
        try:
            transaction_date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid date format'}), 400
        
        # Create new transaction
        transaction = Transaction(
            user_id=current_user.id,
            amount=float(data['amount']),
            category=data['category'],
            date=transaction_date,
            description=data.get('description', ''),
            is_impulse=data.get('is_impulse', False)
        )
        
        db_session.add(transaction)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transaction added successfully',
            'transaction': transaction.to_dict()
        })
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error adding transaction: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    """
    Update an existing transaction
    """
    current_user = get_current_user()
    data = request.get_json()
    
    try:
        transaction = db_session.query(Transaction).filter_by(id=transaction_id, user_id=current_user.id).first()
        
        if not transaction:
            return jsonify({'success': False, 'error': 'Transaction not found'}), 404
        
        # Update fields if provided
        if 'amount' in data:
            transaction.amount = float(data['amount'])
        
        if 'category' in data:
            transaction.category = data['category']
        
        if 'date' in data:
            try:
                transaction.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'success': False, 'error': 'Invalid date format'}), 400
        
        if 'description' in data:
            transaction.description = data['description']
        
        if 'is_impulse' in data:
            transaction.is_impulse = bool(data['is_impulse'])
        
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transaction updated successfully',
            'transaction': transaction.to_dict()
        })
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error updating transaction: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/transactions/convert/<int:transaction_id>', methods=['POST'])
@jwt_required()
def convert_to_saved_impulse(transaction_id):
    """
    Convert a transaction to a saved impulse (redirected to investment)
    """
    current_user = get_current_user()
    
    try:
        transaction = db_session.query(Transaction).filter_by(id=transaction_id, user_id=current_user.id).first()
        
        if not transaction:
            return jsonify({'success': False, 'error': 'Transaction not found'}), 404
        
        # Create a new saved impulse from the transaction
        impulse = SavedImpulse(
            user_id=current_user.id,
            description=transaction.description or f"Redirected {transaction.category} purchase",
            category=transaction.category,
            amount=transaction.amount,
            notes=f"Converted from transaction on {transaction.date.strftime('%Y-%m-%d')}"
        )
        
        # Delete the original transaction
        db_session.delete(transaction)
        
        # Add the new saved impulse
        db_session.add(impulse)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transaction converted to saved impulse successfully',
            'impulse': impulse.to_dict()
        })
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error converting transaction to saved impulse: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/budgets', methods=['GET'])
@jwt_required()
def get_budgets():
    """
    Get all budgets for the current user for the current month
    """
    current_user = get_current_user()
    
    try:
        # Get current month and year
        current_month = request.args.get('month')
        current_year = request.args.get('year')
        
        if not current_month or not current_year:
            current_month = datetime.now().month
            current_year = datetime.now().year
        else:
            current_month = int(current_month)
            current_year = int(current_year)
        
        # Get budgets for current month
        budgets = db_session.query(Budget).filter_by(
            user_id=current_user.id,
            month=current_month,
            year=current_year
        ).all()
        
        # Get transactions for current month
        transactions = db_session.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            extract('month', Transaction.date) == current_month,
            extract('year', Transaction.date) == current_year
        ).all()
        
        # Calculate spending by category
        spending_by_category = {}
        for transaction in transactions:
            category = transaction.category
            if category not in spending_by_category:
                spending_by_category[category] = 0
            spending_by_category[category] += transaction.amount
        
        # Format response
        budget_data = []
        for budget in budgets:
            spent = spending_by_category.get(budget.category, 0)
            remaining = max(0, budget.planned_amount - spent)
            percentage = 0
            if budget.planned_amount > 0:
                percentage = round((spent / budget.planned_amount) * 100, 1)
            
            budget_data.append({
                'id': budget.id,
                'category': budget.category,
                'planned_amount': budget.planned_amount,
                'spent': spent,
                'remaining': remaining,
                'percentage': percentage,
                'status': 'over' if spent > budget.planned_amount else 'under'
            })
        
        # Add categories with spending but no budget
        for category, amount in spending_by_category.items():
            if not any(b.category == category for b in budgets):
                budget_data.append({
                    'id': None,
                    'category': category,
                    'planned_amount': 0,
                    'spent': amount,
                    'remaining': 0,
                    'percentage': 100,
                    'status': 'over'
                })
        
        # Sort by category
        budget_data.sort(key=lambda x: x['category'])
        
        return jsonify({
            'success': True,
            'budgets': budget_data,
            'month': current_month,
            'year': current_year
        })
    
    except Exception as e:
        logger.error(f"Error retrieving budgets: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/budgets', methods=['POST'])
@jwt_required()
def create_budget():
    """
    Create or update a budget for a category
    """
    current_user = get_current_user()
    data = request.get_json()
    
    try:
        # Validate required fields
        required_fields = ['category', 'planned_amount', 'month', 'year']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Parse data
        category = data['category']
        planned_amount = float(data['planned_amount'])
        month = int(data['month'])
        year = int(data['year'])
        
        # Check if budget already exists
        existing_budget = db_session.query(Budget).filter_by(
            user_id=current_user.id,
            category=category,
            month=month,
            year=year
        ).first()
        
        if existing_budget:
            # Update existing budget
            existing_budget.planned_amount = planned_amount
            message = 'Budget updated successfully'
            budget = existing_budget
        else:
            # Create new budget
            budget = Budget(
                user_id=current_user.id,
                category=category,
                planned_amount=planned_amount,
                month=month,
                year=year
            )
            db_session.add(budget)
            message = 'Budget created successfully'
        
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': message,
            'budget': budget.to_dict()
        })
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error creating/updating budget: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/budgets/<int:budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    """
    Delete a budget
    """
    current_user = get_current_user()
    
    try:
        budget = db_session.query(Budget).filter_by(id=budget_id, user_id=current_user.id).first()
        
        if not budget:
            return jsonify({'success': False, 'error': 'Budget not found'}), 404
        
        db_session.delete(budget)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Budget deleted successfully'
        })
    
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error deleting budget: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

@app.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Get all unique spending categories for the current user
    """
    current_user = get_current_user()
    
    try:
        # Get all transactions for the user
        transactions = db_session.query(Transaction.category).filter_by(user_id=current_user.id).distinct().all()
        
        # Get all budgets for the user
        budgets = db_session.query(Budget.category).filter_by(user_id=current_user.id).distinct().all()
        
        # Combine and deduplicate categories
        categories = set([t.category for t in transactions] + [b.category for b in budgets])
        
        # Add default categories if not present
        default_categories = [
            'groceries', 'dining', 'entertainment', 'shopping', 'travel', 
            'utilities', 'housing', 'transportation', 'healthcare', 'education',
            'investments', 'clothing', 'electronics', 'subscriptions', 'gifts',
            'personal care', 'savings'
        ]
        
        for category in default_categories:
            categories.add(category)
        
        # Sort alphabetically
        sorted_categories = sorted(list(categories))
        
        return jsonify({
            'success': True,
            'categories': sorted_categories
        })
    
    except Exception as e:
        logger.error(f"Error retrieving categories: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        db_session.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)