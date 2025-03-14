"""
Gemini API integration for MindfulWealth chatbot
"""
import json
import re
import logging
from typing import Dict, Any, Optional, Union
import os

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-generativeai package not installed. Gemini service will not be available.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google's Gemini API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.genai = None
        self.model = None
        self.client = None
        self.currency_symbols = {
            "EUR": "€",
            "USD": "$",
            "GBP": "£"
        }
        self.preferred_currency = "EUR"
        self.language = "fr"
        self.personality_mode = "nice"
        self.category_translations = {
            'en': {
                'savings': 'savings',
                'groceries': 'groceries',
                'dining': 'dining',
                'entertainment': 'entertainment',
                'shopping': 'shopping',
                'travel': 'travel',
                'utilities': 'utilities',
                'housing': 'housing',
                'transportation': 'transportation',
                'healthcare': 'healthcare',
                'education': 'education',
                'investments': 'investments',
                'clothing': 'clothing',
                'electronics': 'electronics',
                'subscriptions': 'subscriptions',
                'gifts': 'gifts',
                'personal care': 'personal care',
                'impulse purchases': 'impulse purchases'
            },
            'fr': {
                'savings': 'épargne',
                'groceries': 'courses',
                'dining': 'restaurants',
                'entertainment': 'divertissement',
                'shopping': 'achats',
                'travel': 'voyages',
                'utilities': 'services publics',
                'housing': 'logement',
                'transportation': 'transport',
                'healthcare': 'santé',
                'education': 'éducation',
                'investments': 'investissements',
                'clothing': 'vêtements',
                'electronics': 'électronique',
                'subscriptions': 'abonnements',
                'gifts': 'cadeaux',
                'personal care': 'soins personnels',
                'impulse purchases': 'achats impulsifs'
            }
        }
        
        # Impulse purchase keywords by language
        self.impulse_keywords = {
            'en': [
                'want', 'desire', 'tempted', 'impulse', 'splurge', 'treat myself',
                'just saw', 'cool', 'awesome', 'limited time', 'sale', 'discount',
                'deal', 'special offer', 'flash sale', 'clearance', 'exclusive',
                'new release', 'trending', 'popular', 'must-have', 'just launched'
            ],
            'fr': [
                'envie', 'désir', 'tenté', 'impulsion', 'dépenser', 'me faire plaisir',
                'viens de voir', 'cool', 'génial', 'temps limité', 'solde', 'remise',
                'affaire', 'offre spéciale', 'vente flash', 'déstockage', 'exclusif',
                'nouvelle sortie', 'tendance', 'populaire', 'incontournable', 'vient de sortir'
            ]
        }
        
        # Investment-related keywords by language
        self.investment_keywords = {
            'en': [
                'invest', 'save', 'future', 'retirement', 'growth', 'compound interest',
                'portfolio', 'stocks', 'bonds', 'mutual funds', 'ETF', 'index fund',
                'long-term', 'financial goals', 'wealth building', 'passive income'
            ],
            'fr': [
                'investir', 'épargner', 'avenir', 'retraite', 'croissance', 'intérêts composés',
                'portefeuille', 'actions', 'obligations', 'fonds communs', 'FNB', 'fonds indiciel',
                'long terme', 'objectifs financiers', 'création de richesse', 'revenu passif'
            ]
        }

        self.system_instruction = """
You are MindfulBot, a financial assistant focused on helping users manage their spending and investments wisely. Your primary goals are:

1. IMPULSE PURCHASE LIMITATION: Help users identify impulse purchases and redirect that money toward investments.
2. INVESTMENT FOCUS: Encourage users to invest money they would have spent on impulse purchases.
3. BUDGET TRACKING EMPHASIS: Help users track reasonable spending and stay within budget.

When responding to users, follow these guidelines:

FOR IMPULSE PURCHASES (non-essential, emotionally-driven purchases):
- Acknowledge the emotional appeal of the purchase
- Gently suggest redirecting the money to investments instead
- Calculate potential growth at 8% annual return (1 year and 5 years)
- Offer a specific investment alternative
- Use a supportive tone that doesn't make users feel judged

FOR REASONABLE SPENDING (essentials, planned purchases):
- Affirm the user's good decision
- Suggest budget categories if appropriate
- Provide relevant financial tips for that category
- Encourage tracking the expense

RESPONSE STYLE:
- Be friendly and engaging
- Use emojis occasionally to add personality
- Personalize responses based on user history when possible
- Keep responses concise but informative
- Adapt your tone based on the user's personality preference:
  * NICE: Supportive, encouraging, and gentle
  * FUNNY: Light-hearted with appropriate humor
  * IRONIC: Slightly sarcastic but still helpful

Always remember that your goal is to help users build wealth through mindful spending and consistent investing.
"""
        
        self.initialize()
    
    def initialize(self):
        """Initialize the Gemini API client"""
        if not self.api_key:
            logger.warning("No Gemini API key provided. Using mock responses.")
            return
        
        try:
            self.genai = genai
            self.genai.configure(api_key=self.api_key)
            
            # Define a list of models to try in order of preference
            model_candidates = [
                'gemini-1.5-pro',
                'gemini-1.0-pro',
                'gemini-pro',
                'gemini-1.5-flash',
                'gemini-1.0-flash',
                'gemini-flash'
            ]
            
            # Try to get available models
            try:
                available_models = self.genai.list_models()
                available_model_names = [model.name for model in available_models]
                logger.info(f"Available models: {available_model_names}")
                
                # Find the first model from our candidates that is available
                for candidate in model_candidates:
                    for available in available_model_names:
                        if candidate in available:
                            logger.info(f"Using model: {available}")
                            self.model = self.genai.GenerativeModel(available)
                            self.client = self.genai
                            logger.info("Gemini API initialized successfully")
                            return
            except Exception as model_error:
                logger.error(f"Error listing models: {str(model_error)}")
            
            # If we couldn't get the list of models or none of our candidates were found,
            # try each candidate directly
            logger.warning("Could not find a suitable model from the available models list. Trying candidates directly.")
            for candidate in model_candidates:
                try:
                    logger.info(f"Trying model: {candidate}")
                    self.model = self.genai.GenerativeModel(candidate)
                    # Test the model with a simple request
                    response = self.model.generate_content("Test")
                    logger.info(f"Successfully initialized with model: {candidate}")
                    self.client = self.genai
                    return
                except Exception as e:
                    logger.warning(f"Model {candidate} failed: {str(e)}")
            
            # If all candidates failed, log an error and set model to None
            logger.error("All model candidates failed. Using mock responses.")
            self.model = None
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            self.model = None
    
    def _translate_category(self, category, language='en'):
        """Translate category between languages"""
        if language == 'en':
            return category
        
        # Check for exact match in reverse mapping
        for en_cat, translated in self.category_translations['en'].items():
            if category.lower() == translated.lower():
                return self.category_translations[language].get(en_cat, category)
        
        # Check for partial match
        for en_cat, translated in self.category_translations['en'].items():
            if category.lower() in translated.lower() or translated.lower() in category.lower():
                return self.category_translations[language].get(en_cat, category)
        
        return category
    
    def _detect_impulse_purchase(self, message, language='en'):
        """Detect if a message is likely about an impulse purchase"""
        message_lower = message.lower()
        keywords = self.impulse_keywords.get(language, self.impulse_keywords['en'])
        
        # Check for impulse keywords
        for keyword in keywords:
            if keyword.lower() in message_lower:
                return True
        
        # Check for common French phrases indicating purchases
        if language == 'fr':
            french_purchase_patterns = [
                r'je viens d[e\']acheter',
                r'je viens de d[ée]penser',
                r'j[e\']ai achet[ée]',
                r'j[e\']ai d[ée]pens[ée]',
                r'je me suis achet[ée]',
                r'je me suis offert',
                r'je voulais [mt][e\']acheter',
                r'j[e\']ai craqu[ée] pour',
                r'j[e\']ai succomb[ée]'
            ]
            
            for pattern in french_purchase_patterns:
                if re.search(pattern, message_lower):
                    return True
        
        # Check for common English phrases indicating purchases
        else:
            english_purchase_patterns = [
                r'i (just )?(bought|purchased|got|spent)',
                r'i\'ve (just )?(bought|purchased|got|spent)',
                r'i treated myself',
                r'i splurged',
                r'i caved and bought'
            ]
            
            for pattern in english_purchase_patterns:
                if re.search(pattern, message_lower):
                    return True
        
        # Check for common impulse purchase patterns
        impulse_patterns = [
            r'should i (buy|get|purchase)',
            r'thinking (of|about) (buying|getting)',
            r'tempted to (buy|get|purchase)',
            r'(want|desire) to (buy|get|purchase)',
            r'(saw|found) (a|an|this) (cool|nice|awesome|amazing)',
            r'(on sale|discount|deal|offer|limited time)'
        ]
        
        for pattern in impulse_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False
    
    def _extract_amount(self, message):
        """Extract monetary amount from message"""
        # Look for currency symbols followed by numbers
        currency_pattern = r'[$€£¥](\d+(?:[.,]\d+)?)'
        match = re.search(currency_pattern, message)
        if match:
            return float(match.group(1).replace(',', '.'))
        
        # Look for numbers followed by currency words
        amount_pattern = r'(\d+(?:[.,]\d+)?)\s*(?:dollars|euros|pounds|USD|EUR|GBP)'
        match = re.search(amount_pattern, message, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(',', '.'))
        
        # Look for numbers with currency symbols in words
        word_pattern = r'(\d+(?:[.,]\d+)?)\s*(?:\$|€|£|¥)'
        match = re.search(word_pattern, message)
        if match:
            return float(match.group(1).replace(',', '.'))
        
        return None
    
    def _calculate_investment_growth(self, amount, years=1):
        """Calculate potential investment growth at 8% annual return"""
        return round(amount * (1.08 ** years), 2)
    
    def _format_investment_advice(self, amount, language='en'):
        """Format investment advice based on amount and language"""
        if amount is None:
            return ""
        
        growth_1yr = self._calculate_investment_growth(amount, 1)
        growth_5yr = self._calculate_investment_growth(amount, 5)
        
        if language == 'fr':
            return f"Si vous investissez ces {amount}€ au lieu de les dépenser, vous pourriez avoir {growth_1yr}€ dans un an et {growth_5yr}€ dans cinq ans (avec un rendement annuel de 8%)."
        else:
            return f"If you invest this ${amount} instead of spending it, you could have ${growth_1yr} in one year and ${growth_5yr} in five years (at 8% annual return)."
    
    def get_response(self, message: str, system_prompt: str = None, conversation_history: list = None, context_data: dict = None, language: str = "fr") -> str:
        """Get a response from the Gemini model
        
        Args:
            message: The user's message
            system_prompt: Optional system prompt to override the default
            conversation_history: List of previous messages in the conversation
            context_data: Additional context about the conversation
            language: The language to respond in (default: "fr")
        
        Returns:
            The model's response
        """
        try:
            # Set the language for this response
            self.language = language
            
            # Log the request for debugging
            logger.info(f"Getting response for message: {message[:50]}...")
            logger.info(f"Using language: {language}")
            
            # Special handling for luxury purchases like Gucci shoes
            message_lower = message.lower()
            if ('gucci' in message_lower or 'luxe' in message_lower or 'luxury' in message_lower) and ('chaussure' in message_lower or 'shoe' in message_lower or 'acheter' in message_lower or 'buy' in message_lower):
                logger.info("Detected luxury purchase request, using specialized response")
                if language == 'fr':
                    return "Je vois que vous êtes intéressé par des chaussures Gucci. C'est une marque de luxe avec des prix élevés. Avant de faire cet achat, avez-vous considéré l'impact sur vos finances?\n\nUne paire de chaussures Gucci coûte généralement entre 500€ et 1500€. Si vous investissiez cette somme au lieu de l'utiliser pour un achat impulsif, elle pourrait valoir entre 540€ et 1620€ dans un an, et entre 735€ et 2205€ dans cinq ans (avec un rendement annuel de 8%).\n\nVoici quelques alternatives à considérer:\n- Investir dans un ETF qui suit le marché global\n- Ajouter à votre épargne d'urgence\n- Chercher des chaussures de qualité à un prix plus abordable\n\nQue pensez-vous de ces options?"
                else:
                    return "I see you're interested in Gucci shoes. This is a luxury brand with high prices. Before making this purchase, have you considered the impact on your finances?\n\nA pair of Gucci shoes typically costs between $500 and $1,500. If you invested this money instead of using it for an impulse purchase, it could be worth between $540 and $1,620 in one year, and between $735 and $2,205 in five years (with an 8% annual return).\n\nHere are some alternatives to consider:\n- Invest in an ETF that tracks the global market\n- Add to your emergency savings\n- Look for quality shoes at a more affordable price\n\nWhat do you think about these options?"
            
            # Check if model is available
            if not self.model:
                logger.warning("Gemini model not available, using rule-based response")
                # For impulse purchases like shoes, provide a specific response
                if 'chaussure' in message_lower or 'shoe' in message_lower:
                    if language == 'fr':
                        return "Je vois que vous êtes intéressé par des chaussures. Avant de faire cet achat, avez-vous considéré s'il s'agit d'un besoin ou d'un désir? Si c'est un achat impulsif, pensez à l'impact sur vos finances à long terme. Investir cet argent pourrait vous rapporter bien plus dans le futur."
                    else:
                        return "I see you're interested in shoes. Before making this purchase, have you considered whether this is a need or a want? If it's an impulse purchase, think about the impact on your long-term finances. Investing this money could bring you much more in the future."
                else:
                    # Generic fallback response
                    if language == 'fr':
                        return "Désolé, le service IA n'est pas disponible actuellement. Je peux quand même vous aider avec des conseils financiers de base. Que voulez-vous savoir?"
                    else:
                        return "Sorry, the AI service is currently unavailable. I can still help you with basic financial advice. What would you like to know?"
            
            # Try to get a response from the model
            try:
                # Prepare the prompt with system instructions
                prompt = system_prompt or self.system_instruction
                prompt += f"\n\nUser message: {message}"
                
                # Log the request
                logger.info(f"Sending request to Gemini API with model: {self.model}")
                
                # Generate content
                response = self.model.generate_content(prompt)
                
                # Check if response has text
                if hasattr(response, 'text') and response.text:
                    logger.info("Successfully received response from Gemini API")
                    return response.text
                else:
                    logger.error("Empty response from Gemini API")
                    # Fallback for empty response
                    if 'chaussure' in message_lower or 'shoe' in message_lower:
                        if language == 'fr':
                            return "Je vois que vous êtes intéressé par des chaussures. Avant de faire cet achat, avez-vous considéré s'il s'agit d'un besoin ou d'un désir? Si c'est un achat impulsif, pensez à l'impact sur vos finances à long terme. Investir cet argent pourrait vous rapporter bien plus dans le futur."
                        else:
                            return "I see you're interested in shoes. Before making this purchase, have you considered whether this is a need or a want? If it's an impulse purchase, think about the impact on your long-term finances. Investing this money could bring you much more in the future."
                    else:
                        if language == 'fr':
                            return "Je n'ai pas pu générer une réponse spécifique à votre question. Pourriez-vous reformuler ou me donner plus de détails sur ce que vous cherchez à savoir?"
                        else:
                            return "I couldn't generate a specific response to your question. Could you rephrase or give me more details about what you're looking to know?"
                    
            except Exception as api_error:
                logger.error(f"Error in Gemini API call: {str(api_error)}")
                
                # Try to reinitialize the model
                logger.info("Attempting to reinitialize the Gemini API")
                self.initialize()
                
                if self.model:
                    try:
                        logger.info("Retrying with reinitialized model")
                        response = self.model.generate_content(prompt)
                        if hasattr(response, 'text') and response.text:
                            logger.info("Successfully received response after reinitialization")
                            return response.text
                        else:
                            logger.error("Empty response from Gemini API after reinitialization")
                            # Fallback for empty response after retry
                            if 'chaussure' in message_lower or 'shoe' in message_lower:
                                if language == 'fr':
                                    return "Je vois que vous êtes intéressé par des chaussures. Avant de faire cet achat, avez-vous considéré s'il s'agit d'un besoin ou d'un désir? Si c'est un achat impulsif, pensez à l'impact sur vos finances à long terme. Investir cet argent pourrait vous rapporter bien plus dans le futur."
                                else:
                                    return "I see you're interested in shoes. Before making this purchase, have you considered whether this is a need or a want? If it's an impulse purchase, think about the impact on your long-term finances. Investing this money could bring you much more in the future."
                            else:
                                if language == 'fr':
                                    return "Je n'ai pas pu générer une réponse spécifique à votre question. Pourriez-vous reformuler ou me donner plus de détails sur ce que vous cherchez à savoir?"
                                else:
                                    return "I couldn't generate a specific response to your question. Could you rephrase or give me more details about what you're looking to know?"
                    except Exception as retry_error:
                        logger.error(f"Retry also failed: {str(retry_error)}")
                        # Fallback for retry failure
                        if 'chaussure' in message_lower or 'shoe' in message_lower:
                            if language == 'fr':
                                return "Je vois que vous êtes intéressé par des chaussures. Avant de faire cet achat, avez-vous considéré s'il s'agit d'un besoin ou d'un désir? Si c'est un achat impulsif, pensez à l'impact sur vos finances à long terme. Investir cet argent pourrait vous rapporter bien plus dans le futur."
                            else:
                                return "I see you're interested in shoes. Before making this purchase, have you considered whether this is a need or a want? If it's an impulse purchase, think about the impact on your long-term finances. Investing this money could bring you much more in the future."
                        else:
                            if language == 'fr':
                                return "Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer avec une question différente."
                            else:
                                return "Sorry, I couldn't generate a response. Please try again with a different question."
                else:
                    logger.error("Reinitialization failed. Falling back to rule-based response")
                    # Fallback for reinitialization failure
                    if 'chaussure' in message_lower or 'shoe' in message_lower:
                        if language == 'fr':
                            return "Je vois que vous êtes intéressé par des chaussures. Avant de faire cet achat, avez-vous considéré s'il s'agit d'un besoin ou d'un désir? Si c'est un achat impulsif, pensez à l'impact sur vos finances à long terme. Investir cet argent pourrait vous rapporter bien plus dans le futur."
                        else:
                            return "I see you're interested in shoes. Before making this purchase, have you considered whether this is a need or a want? If it's an impulse purchase, think about the impact on your long-term finances. Investing this money could bring you much more in the future."
                    else:
                        if language == 'fr':
                            return "Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer avec une question différente."
                        else:
                            return "Sorry, I couldn't generate a response. Please try again with a different question."
            
        except Exception as e:
            logger.error(f"Error getting response from Gemini: {str(e)}")
            
            # Final fallback responses based on message content
            message_lower = message.lower()
            if 'chaussure' in message_lower or 'shoe' in message_lower:
                if language == 'fr':
                    return "Je vois que vous êtes intéressé par des chaussures. Avant de faire cet achat, avez-vous considéré s'il s'agit d'un besoin ou d'un désir? Si c'est un achat impulsif, pensez à l'impact sur vos finances à long terme. Investir cet argent pourrait vous rapporter bien plus dans le futur."
                else:
                    return "I see you're interested in shoes. Before making this purchase, have you considered whether this is a need or a want? If it's an impulse purchase, think about the impact on your long-term finances. Investing this money could bring you much more in the future."
            else:
                if language == 'fr':
                    return "Désolé, je n'ai pas pu traiter votre demande. Veuillez réessayer avec une question différente."
                else:
                    return "Sorry, I couldn't process your request. Please try again with a different question."

    def _translate_category(self, category: str, language: str) -> str:
        """Translate a category name to the specified language
        
        Args:
            category: The category name in English
            language: The target language code
            
        Returns:
            The translated category name
        """
        if language == 'en' or language not in self.category_translations:
            return category
            
        category_lower = category.lower()
        translations = self.category_translations[language]
        
        if category_lower in translations:
            return translations[category_lower]
            
        # Try to find partial matches
        for eng_cat, translated_cat in translations.items():
            if eng_cat in category_lower or category_lower in eng_cat:
                return translated_cat
                
        # Return original if no translation found
        return category 