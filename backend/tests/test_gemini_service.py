import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.gemini_service import GeminiService, GENAI_AVAILABLE

class TestGeminiService(unittest.TestCase):
    """Test cases for the GeminiService class"""

    def setUp(self):
        """Set up test environment"""
        # Use a test API key for testing
        self.test_api_key = "test_api_key"
        
        # Create a mock for the GenerativeModel
        self.mock_model = MagicMock()
        self.mock_response = MagicMock()
        self.mock_response.text = "This is a test response from Gemini"
        self.mock_model.generate_content.return_value = self.mock_response
        
        # Create a mock for the genai module
        self.mock_genai = MagicMock()
        self.mock_genai.GenerativeModel.return_value = self.mock_model

    @patch('services.gemini_service.GENAI_AVAILABLE', True)
    @patch('google.generativeai.configure')
    def test_initialization_with_api_key(self, mock_configure):
        """Test initialization with API key"""
        with patch('services.gemini_service.genai', self.mock_genai):
            service = GeminiService(api_key=self.test_api_key)
            
            # Check if the API key was set
            self.assertEqual(service.api_key, self.test_api_key)
            
            # Check if the genai module was configured
            mock_configure.assert_called_once_with(api_key=self.test_api_key)
            
            # Check if the model was created
            self.mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
            
            # Check if the model was set
            self.assertEqual(service.model, self.mock_model)

    @patch('services.gemini_service.GENAI_AVAILABLE', False)
    def test_initialization_without_genai(self):
        """Test initialization when genai is not available"""
        service = GeminiService(api_key=self.test_api_key)
        
        # Check if the API key was set
        self.assertEqual(service.api_key, self.test_api_key)
        
        # Check if the model is None
        self.assertIsNone(service.model)

    @patch('services.gemini_service.GENAI_AVAILABLE', True)
    def test_analyze_message_with_genai(self):
        """Test analyze_message with genai available"""
        with patch('services.gemini_service.genai', self.mock_genai):
            service = GeminiService(api_key=self.test_api_key)
            service.model = self.mock_model
            
            # Call analyze_message
            result = service.analyze_message("Test message")
            
            # Check if the model was called
            self.mock_model.generate_content.assert_called_once()
            
            # Check if the response was returned
            self.assertEqual(result['response'], "This is a test response from Gemini")

    @patch('services.gemini_service.GENAI_AVAILABLE', False)
    def test_analyze_message_without_genai(self):
        """Test analyze_message when genai is not available"""
        service = GeminiService(api_key=self.test_api_key)
        
        # Mock the _analyze_message_rule_based method
        service._analyze_message_rule_based = MagicMock(return_value={
            'is_impulse': True,
            'amount': 100,
            'category': 'shoes',
            'response': 'Rule-based response',
            'financial_data': {'type': 'impulse'}
        })
        
        # Call analyze_message
        result = service.analyze_message("Test message")
        
        # Check if _analyze_message_rule_based was called
        service._analyze_message_rule_based.assert_called_once_with("Test message")
        
        # Check if the response was returned
        self.assertEqual(result['response'], 'Rule-based response')
        self.assertTrue(result['is_impulse'])
        self.assertEqual(result['amount'], 100)
        self.assertEqual(result['category'], 'shoes')

    def test_detect_impulse_purchase(self):
        """Test _detect_impulse_purchase method"""
        service = GeminiService()
        
        # Test with impulse purchase message in English
        self.assertTrue(service._detect_impulse_purchase("I just bought new shoes", "en"))
        self.assertTrue(service._detect_impulse_purchase("I want to buy a new phone", "en"))
        self.assertTrue(service._detect_impulse_purchase("I'm thinking about getting a new TV", "en"))
        
        # Test with impulse purchase message in French
        self.assertTrue(service._detect_impulse_purchase("Je viens d'acheter des chaussures", "fr"))
        self.assertTrue(service._detect_impulse_purchase("Je veux acheter un nouveau téléphone", "fr"))
        
        # Test with non-impulse purchase message
        self.assertFalse(service._detect_impulse_purchase("What's the weather today?", "en"))
        self.assertFalse(service._detect_impulse_purchase("Quel temps fait-il aujourd'hui?", "fr"))

    def test_extract_amount(self):
        """Test _extract_amount method"""
        service = GeminiService()
        
        # Test with amount in different formats
        self.assertEqual(service._extract_amount("I spent $100 on shoes"), 100)
        self.assertEqual(service._extract_amount("J'ai dépensé 100€ pour des chaussures"), 100)
        self.assertEqual(service._extract_amount("It costs 99.99 euros"), 99.99)
        
        # Test with no amount
        self.assertIsNone(service._extract_amount("I bought some shoes"))

    def test_calculate_investment_growth(self):
        """Test _calculate_investment_growth method"""
        service = GeminiService()
        
        # Test with different amounts and years
        self.assertEqual(service._calculate_investment_growth(100, 1), 108)
        self.assertEqual(service._calculate_investment_growth(100, 5), 146.93)
        
        # Test with zero amount
        self.assertEqual(service._calculate_investment_growth(0, 1), 0)

    def test_is_investment_question(self):
        """Test _is_investment_question method"""
        service = GeminiService()
        
        # Test with investment question in English
        self.assertTrue(service._is_investment_question("How should I invest 1000 euros?"))
        self.assertTrue(service._is_investment_question("What are good investment options?"))
        
        # Test with investment question in French
        self.assertTrue(service._is_investment_question("Comment investir 1000 euros?"))
        self.assertTrue(service._is_investment_question("Quelles sont les bonnes options d'investissement?"))
        
        # Test with non-investment question
        self.assertFalse(service._is_investment_question("What's the weather today?"))
        self.assertFalse(service._is_investment_question("Quel temps fait-il aujourd'hui?"))

    def test_format_currency(self):
        """Test _format_currency method"""
        service = GeminiService()
        
        # Test with different currencies
        self.assertEqual(service._format_currency(100), "€100.00")
        self.assertEqual(service._format_currency(100, "USD"), "$100.00")
        self.assertEqual(service._format_currency(100, "GBP"), "£100.00")
        
        # Test with default currency
        service.preferred_currency = "USD"
        self.assertEqual(service._format_currency(100), "$100.00")

if __name__ == '__main__':
    unittest.main() 