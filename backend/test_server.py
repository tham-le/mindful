from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
preferred_currency = "EUR"  # Default currency is EUR
personality_mode = "balanced"  # Default personality mode

@app.route('/')
def hello():
    return "MindfulWealth API is running!"

@app.route('/api/currency', methods=['GET', 'POST'])
def currency():
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

@app.route('/api/personality', methods=['POST'])
def personality():
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

@app.route('/api/chat', methods=['POST'])
def chat():
    """Simple mock chat endpoint"""
    data = request.json
    message = data.get('message', '')
    
    # Simple mock response
    response = f"You said: {message}. This is a test response from the backend."
    
    return jsonify({
        'response': response,
        'financial_data': None
    })

@app.route('/api/transactions', methods=['GET'])
def transactions():
    """Get mock transactions"""
    mock_transactions = [
        {
            'id': 1,
            'amount': 100.0,
            'category': 'Food',
            'date': '2023-03-01T12:00:00',
            'description': 'Grocery shopping'
        },
        {
            'id': 2,
            'amount': 50.0,
            'category': 'Entertainment',
            'date': '2023-03-02T18:30:00',
            'description': 'Movie tickets'
        }
    ]
    
    return jsonify(mock_transactions)

@app.route('/api/budget', methods=['GET'])
def budget():
    """Get mock budget"""
    mock_budget = {
        'total': 1000.0,
        'spent': 500.0,
        'categories': [
            {
                'name': 'Food',
                'planned': 300.0,
                'actual': 250.0
            },
            {
                'name': 'Entertainment',
                'planned': 200.0,
                'actual': 150.0
            },
            {
                'name': 'Transportation',
                'planned': 150.0,
                'actual': 100.0
            }
        ]
    }
    
    return jsonify(mock_budget)

@app.route('/api/saved-impulses', methods=['GET'])
def saved_impulses():
    """Get mock saved impulses"""
    mock_impulses = [
        {
            'id': 1,
            'item': 'Designer shoes',
            'amount': 200.0,
            'category': 'Clothing',
            'date': '2023-03-01T12:00:00',
            'potential_value': 216.0
        },
        {
            'id': 2,
            'item': 'Smart watch',
            'amount': 300.0,
            'category': 'Electronics',
            'date': '2023-03-02T18:30:00',
            'potential_value': 324.0
        }
    ]
    
    return jsonify(mock_impulses)

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Get mock dashboard data"""
    mock_dashboard = {
        'total_spent': 500.0,
        'total_budget': 1000.0,
        'total_saved': 500.0,
        'potential_growth': 540.0,
        'categories': [
            {
                'name': 'Food',
                'spent': 250.0,
                'budget': 300.0
            },
            {
                'name': 'Entertainment',
                'spent': 150.0,
                'budget': 200.0
            },
            {
                'name': 'Transportation',
                'spent': 100.0,
                'budget': 150.0
            }
        ],
        'recent_transactions': [
            {
                'id': 1,
                'amount': 100.0,
                'category': 'Food',
                'date': '2023-03-01T12:00:00',
                'description': 'Grocery shopping'
            },
            {
                'id': 2,
                'amount': 50.0,
                'category': 'Entertainment',
                'date': '2023-03-02T18:30:00',
                'description': 'Movie tickets'
            }
        ],
        'saved_impulses': [
            {
                'id': 1,
                'item': 'Designer shoes',
                'amount': 200.0,
                'category': 'Clothing',
                'date': '2023-03-01T12:00:00',
                'potential_value': 216.0
            },
            {
                'id': 2,
                'item': 'Smart watch',
                'amount': 300.0,
                'category': 'Electronics',
                'date': '2023-03-02T18:30:00',
                'potential_value': 324.0
            }
        ]
    }
    
    return jsonify(mock_dashboard)

if __name__ == '__main__':
    print("Starting test server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 