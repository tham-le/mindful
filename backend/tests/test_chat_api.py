import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app
from models import User, Transaction, Budget, SavedImpulse
from services.gemini_service import GeminiService

class TestChatAPI(unittest.TestCase):
    """Test cases for the chat API endpoints"""

    def setUp(self):
        """Set up test environment"""
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        # Create a mock user
        self.mock_user = MagicMock(spec=User)
        self.mock_user.id = 1
        self.mock_user.name = "Test User"
        self.mock_user.email = "test@example.com"
        
        # Create a mock JWT token
        self.mock_token = "mock_token"
        
        # Create a patch for the get_current_user function
        self.get_current_user_patcher = patch('app.get_current_user')
        self.mock_get_current_user = self.get_current_user_patcher.start()
        self.mock_get_current_user.return_value = self.mock_user
        
        # Create a patch for the jwt_required decorator
        self.jwt_required_patcher = patch('app.jwt_required')
        self.mock_jwt_required = self.jwt_required_patcher.start()
        
        # Create a patch for the db_session
        self.db_session_patcher = patch('app.db_session')
        self.mock_db_session = self.db_session_patcher.start()
        
        # Create a patch for the GeminiService
        self.gemini_service_patcher = patch('app.gemini_service')
        self.mock_gemini_service = self.gemini_service_patcher.start()
        
        # Set up mock response from GeminiService
        self.mock_gemini_service.analyze_message.return_value = {
            'is_impulse': True,
            'amount': 100.0,
            'category': 'shoes',
            'response': 'I see you want to buy shoes for 100€. Would you like to save this money instead?',
            'financial_data': {
                'type': 'impulse',
                'amount': 100.0,
                'category': 'shoes',
                'potential_value_1yr': 108.0,
                'potential_value_5yr': 146.93
            }
        }
        
        # Set up mock query results
        self.mock_query = MagicMock()
        self.mock_db_session.query.return_value = self.mock_query
        self.mock_query.filter.return_value = self.mock_query
        self.mock_query.filter_by.return_value = self.mock_query
        self.mock_query.first.return_value = None
        
    def tearDown(self):
        """Clean up after tests"""
        self.get_current_user_patcher.stop()
        self.jwt_required_patcher.stop()
        self.db_session_patcher.stop()
        self.gemini_service_patcher.stop()

    def test_chat_endpoint_with_impulse_purchase(self):
        """Test the /api/chat endpoint with an impulse purchase message"""
        # Set up the request data
        request_data = {
            'message': 'I want to buy shoes for 100€',
            'contextData': None,
            'conversationHistory': []
        }
        
        # Make the request
        response = self.client.post('/api/chat', json=request_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('response', data)
        self.assertIn('financial_data', data)
        
        # Check that the GeminiService was called
        self.mock_gemini_service.analyze_message.assert_called_once_with(
            'I want to buy shoes for 100€',
            conversation_history=[],
            context_data=None
        )
        
        # Check the financial data
        financial_data = data['financial_data']
        self.assertEqual(financial_data['type'], 'impulse')
        self.assertEqual(financial_data['amount'], 100.0)
        self.assertEqual(financial_data['category'], 'shoes')
        self.assertEqual(financial_data['potential_value_1yr'], 108.0)
        self.assertEqual(financial_data['potential_value_5yr'], 146.93)

    def test_chat_endpoint_with_save_impulse_command(self):
        """Test the /api/chat endpoint with a command to save an impulse purchase"""
        # Set up the request data with a command to save an impulse purchase
        request_data = {
            'message': 'save impulse shoes 100€',
            'contextData': None,
            'conversationHistory': []
        }
        
        # Set up mock response from GeminiService for a save impulse command
        self.mock_gemini_service.analyze_message.return_value = {
            'is_impulse': True,
            'amount': 100.0,
            'category': 'shoes',
            'response': 'I have saved your impulse purchase of 100€ for shoes. This will grow to 108€ in one year!',
            'financial_data': {
                'type': 'impulse',
                'amount': 100.0,
                'category': 'shoes',
                'potential_value_1yr': 108.0,
                'potential_value_5yr': 146.93,
                'command': 'save_impulse'
            }
        }
        
        # Make the request
        response = self.client.post('/api/chat', json=request_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('response', data)
        self.assertIn('financial_data', data)
        
        # Check that the GeminiService was called
        self.mock_gemini_service.analyze_message.assert_called_once_with(
            'save impulse shoes 100€',
            conversation_history=[],
            context_data=None
        )
        
        # Check that a SavedImpulse was added to the database
        self.mock_db_session.add.assert_called_once()
        self.mock_db_session.commit.assert_called_once()

    def test_chat_endpoint_with_add_transaction_command(self):
        """Test the /api/chat endpoint with a command to add a transaction"""
        # Set up the request data with a command to add a transaction
        request_data = {
            'message': 'add transaction groceries 50€',
            'contextData': None,
            'conversationHistory': []
        }
        
        # Set up mock response from GeminiService for an add transaction command
        self.mock_gemini_service.analyze_message.return_value = {
            'is_impulse': False,
            'amount': 50.0,
            'category': 'groceries',
            'response': 'I have added a transaction of 50€ for groceries.',
            'financial_data': {
                'type': 'reasonable',
                'amount': 50.0,
                'category': 'groceries',
                'command': 'add_transaction'
            }
        }
        
        # Make the request
        response = self.client.post('/api/chat', json=request_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('response', data)
        self.assertIn('financial_data', data)
        
        # Check that the GeminiService was called
        self.mock_gemini_service.analyze_message.assert_called_once_with(
            'add transaction groceries 50€',
            conversation_history=[],
            context_data=None
        )
        
        # Check that a Transaction was added to the database
        self.mock_db_session.add.assert_called_once()
        self.mock_db_session.commit.assert_called_once()

    def test_chat_endpoint_with_add_budget_command(self):
        """Test the /api/chat endpoint with a command to add a budget"""
        # Set up the request data with a command to add a budget
        request_data = {
            'message': 'set budget groceries 500€',
            'contextData': None,
            'conversationHistory': []
        }
        
        # Set up mock response from GeminiService for an add budget command
        self.mock_gemini_service.analyze_message.return_value = {
            'is_impulse': False,
            'amount': 500.0,
            'category': 'groceries',
            'response': 'I have set your budget for groceries to 500€ for this month.',
            'financial_data': {
                'type': 'budget',
                'amount': 500.0,
                'category': 'groceries',
                'command': 'set_budget'
            }
        }
        
        # Make the request
        response = self.client.post('/api/chat', json=request_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('response', data)
        self.assertIn('financial_data', data)
        
        # Check that the GeminiService was called
        self.mock_gemini_service.analyze_message.assert_called_once_with(
            'set budget groceries 500€',
            conversation_history=[],
            context_data=None
        )
        
        # Check that a Budget was added to the database
        self.mock_db_session.add.assert_called_once()
        self.mock_db_session.commit.assert_called_once()

    def test_chat_endpoint_with_investment_question(self):
        """Test the /api/chat endpoint with an investment question"""
        # Set up the request data with an investment question
        request_data = {
            'message': 'How should I invest 1000€?',
            'contextData': None,
            'conversationHistory': []
        }
        
        # Set up mock response from GeminiService for an investment question
        self.mock_gemini_service.analyze_message.return_value = {
            'is_impulse': False,
            'amount': 1000.0,
            'category': None,
            'response': 'For 1000€, I recommend investing in a low-cost index ETF that tracks the global market. This provides diversification and has historically returned around 8% annually.',
            'financial_data': {
                'type': 'investment',
                'amount': 1000.0,
                'potential_value_1yr': 1080.0,
                'potential_value_5yr': 1469.3
            }
        }
        
        # Make the request
        response = self.client.post('/api/chat', json=request_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('response', data)
        self.assertIn('financial_data', data)
        
        # Check that the GeminiService was called
        self.mock_gemini_service.analyze_message.assert_called_once_with(
            'How should I invest 1000€?',
            conversation_history=[],
            context_data=None
        )
        
        # Check the financial data
        financial_data = data['financial_data']
        self.assertEqual(financial_data['type'], 'investment')
        self.assertEqual(financial_data['amount'], 1000.0)
        self.assertEqual(financial_data['potential_value_1yr'], 1080.0)
        self.assertEqual(financial_data['potential_value_5yr'], 1469.3)

    def test_personality_endpoint(self):
        """Test the /api/personality endpoint"""
        # Set up the request data
        request_data = {
            'mode': 'funny'
        }
        
        # Make the request
        response = self.client.post('/api/personality', json=request_data)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the structure of the response
        self.assertIn('success', data)
        self.assertIn('message', data)
        self.assertIn('mode', data)
        
        # Check that the personality mode was set
        self.assertEqual(data['mode'], 'funny')
        self.mock_gemini_service.set_personality_mode.assert_called_once_with('funny')
        
        # Check that the user's personality preference was updated
        self.mock_db_session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main() 