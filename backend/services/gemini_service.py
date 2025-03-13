"""
Gemini API integration for MindfulWealth chatbot
"""
import json
import re
import logging
from typing import Dict, Any, Optional, Union
import os

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-genai package not installed. Gemini service will not be available.")

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
            import google.generativeai as genai
            self.genai = genai
            self.genai.configure(api_key=self.api_key)
            self.model = self.genai.GenerativeModel('gemini-pro')
            self.client = self.genai
            logger.info("Gemini API initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
    
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
    
    def get_response(self, message, context=None, personality_mode='nice', language='en'):
        """Get a response from the Gemini API"""
        if not self.model:
            return self._get_mock_response(message, context, personality_mode, language)
        
        try:
            # Prepare context for the model
            history = []
            if context:
                for msg in context:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})
            
            # Detect if this is likely an impulse purchase
            is_impulse = self._detect_impulse_purchase(message, language)
            amount = self._extract_amount(message)
            
            # Add investment advice if it's an impulse purchase
            investment_advice = ""
            if is_impulse and amount:
                investment_advice = self._format_investment_advice(amount, language)
            
            # Prepare the chat
            chat = self.model.start_chat(history=history)
            
            # Add system instruction
            prompt = f"{self.system_instruction}\n\nUser personality preference: {personality_mode.upper()}\nUser language: {language}\n"
            
            if is_impulse:
                prompt += "\nThis appears to be about an IMPULSE PURCHASE. Remember to gently redirect toward investment.\n"
                if investment_advice:
                    prompt += f"\n{investment_advice}\n"
            
            prompt += f"\nUser message: {message}"
            
            # Get response
            response = chat.send_message(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error getting response from Gemini: {str(e)}")
            return self._get_mock_response(message, context, personality_mode, language)
    
    def _get_mock_response(self, message, context=None, personality_mode='nice', language='en'):
        """Generate a mock response for testing without API"""
        # Detect if this is likely an impulse purchase
        is_impulse = self._detect_impulse_purchase(message, language)
        amount = self._extract_amount(message)
        
        # Extract category if mentioned
        category_match = re.search(r'for\s+(\w+)', message)
        category = category_match.group(1) if category_match else None
        
        if category:
            category = self._translate_category(category, language)
        
        # Basic responses based on personality mode
        if is_impulse:
            if language == 'fr':
                if personality_mode == 'nice':
                    response = f"Je comprends que vous soyez tenté(e) par cet achat. Avez-vous envisagé d'investir cet argent à la place?"
                elif personality_mode == 'funny':
                    response = f"Oh là là, votre portefeuille vient de crier 'Au secours!' 😂 Et si on investissait cet argent à la place?"
                else:  # ironic
                    response = f"Bien sûr, parce que c'est exactement ce dont vous avez besoin... Ou peut-être investir cet argent serait plus judicieux?"
            else:
                if personality_mode == 'nice':
                    response = f"I understand you're tempted by this purchase. Have you considered investing this money instead?"
                elif personality_mode == 'funny':
                    response = f"Whoa there, I can hear your wallet screaming for help! 😂 What if we invest that money instead?"
                else:  # ironic
                    response = f"Sure, because that's exactly what you need right now... Or maybe investing that money would be wiser?"
            
            # Add investment advice if amount is detected
            if amount:
                growth_1yr = self._calculate_investment_growth(amount, 1)
                growth_5yr = self._calculate_investment_growth(amount, 5)
                
                if language == 'fr':
                    response += f"\n\nSi vous investissez ces {amount}€ au lieu de les dépenser, vous pourriez avoir {growth_1yr}€ dans un an et {growth_5yr}€ dans cinq ans (avec un rendement annuel de 8%)."
                else:
                    response += f"\n\nIf you invest this ${amount} instead of spending it, you could have ${growth_1yr} in one year and ${growth_5yr} in five years (at 8% annual return)."
        else:
            if category:
                if language == 'fr':
                    if personality_mode == 'nice':
                        response = f"C'est une bonne idée de suivre vos dépenses pour {category}. Avez-vous un budget mensuel pour cette catégorie?"
                    elif personality_mode == 'funny':
                        response = f"Ah, {category}! L'argent s'envole, mais au moins vous savez où il va! 😄 Avez-vous défini un budget?"
                    else:  # ironic
                        response = f"Dépenser pour {category}, quelle surprise... Avez-vous au moins un budget pour ça?"
                else:
                    if personality_mode == 'nice':
                        response = f"It's a good idea to track your spending on {category}. Do you have a monthly budget for this category?"
                    elif personality_mode == 'funny':
                        response = f"Ah, {category}! Money flies, but at least you know where it's going! 😄 Do you have a budget set?"
                    else:  # ironic
                        response = f"Spending on {category}, what a surprise... Do you at least have a budget for that?"
            else:
                if language == 'fr':
                    if personality_mode == 'nice':
                        response = "Je suis là pour vous aider à gérer vos finances. Comment puis-je vous aider aujourd'hui?"
                    elif personality_mode == 'funny':
                        response = "Bonjour! Je suis votre assistant financier, prêt à faire danser vos euros! 💃 Comment puis-je vous aider?"
                    else:  # ironic
                        response = "Ah, encore besoin d'aide avec votre argent? Quelle surprise... Comment puis-je vous aider cette fois?"
                else:
                    if personality_mode == 'nice':
                        response = "I'm here to help you manage your finances. How can I assist you today?"
                    elif personality_mode == 'funny':
                        response = "Hello there! I'm your financial assistant, ready to make your dollars dance! 💃 How can I help?"
                    else:  # ironic
                        response = "Ah, need help with your money again? What a surprise... How can I assist you this time?"
        
        return response

    def set_personality_mode(self, mode: str) -> None:
        """Set the personality mode for responses
        
        Args:
            mode: One of "nice", "funny", or "irony"
        """
        if mode.lower() in ["nice", "funny", "irony"]:
            self.personality_mode = mode.lower()
            logger.info(f"Personality mode set to: {self.personality_mode}")
        else:
            logger.warning(f"Invalid personality mode: {mode}. Using default 'nice' mode.")
            self.personality_mode = "nice"
    
    def set_preferred_currency(self, currency: str) -> None:
        """Set the preferred currency for responses
        
        Args:
            currency: One of "EUR", "GBP", "USD"
        """
        if currency in ["EUR", "GBP", "USD"]:
            self.preferred_currency = currency
            logger.info(f"Preferred currency set to: {self.preferred_currency}")
        else:
            logger.warning(f"Invalid currency: {currency}. Using default 'EUR'.")
            self.preferred_currency = "EUR"

    def analyze_message(self, message: str, conversation_history: list = None, context_data: dict = None) -> Dict[str, Any]:
        """
        Analyze a message to extract financial information and determine if it's an impulse purchase
        """
        logger.info(f"Analyzing message: {message[:50]}...")
        
        # Check if this is an investment question
        is_investment_question = self._is_investment_question(message)
        
        # Try to use the AI model first, even if it's an investment question
        if GENAI_AVAILABLE and self.model:
            try:
                # Prepare conversation history for context
                history_prompt = ""
                if conversation_history and len(conversation_history) > 0:
                    history_prompt = "CONVERSATION HISTORY:\n"
                    for i, msg in enumerate(conversation_history[-5:]):  # Use last 5 messages for context
                        role = "USER" if msg["role"] == "user" else "ASSISTANT"
                        history_prompt += f"{role}: {msg['content']}\n"
                
                # Prepare context data if available
                context_prompt = ""
                if context_data:
                    context_prompt = "CONTEXT DATA:\n"
                    for key, value in context_data.items():
                        context_prompt += f"{key}: {value}\n"
                
                # Set personality instruction based on mode
                personality_instruction = "Respond in a helpful, friendly manner."
                if hasattr(self, 'personality_mode'):
                    if self.personality_mode == 'funny':
                        personality_instruction = "Respond with light humor while being helpful."
                    elif self.personality_mode == 'irony':
                        personality_instruction = "Respond with a touch of irony while being helpful."
                
                # Add special instructions for investment questions
                special_instructions = ""
                if is_investment_question:
                    special_instructions = """
This is an INVESTMENT QUESTION. Provide detailed, educational advice about investing:
- Explain different investment options (ETFs, index funds, stocks, bonds)
- Mention the importance of diversification and long-term thinking
- Provide specific examples of how to get started with the amount mentioned
- Explain the concept of compound interest with concrete examples
- Mention potential risks and how to mitigate them
"""
                
                # Combine all context for the model with clear section separators
                full_prompt = f"""
{history_prompt}
{context_prompt}
CURRENT USER MESSAGE:
{message}

INSTRUCTIONS:
{personality_instruction}
{special_instructions}
1. Consider the ENTIRE conversation history when crafting your response
2. Maintain continuity with previous messages and reference specific details from earlier in the conversation
3. If this is a follow-up to a previous financial discussion, acknowledge that context explicitly
4. Extract financial information, classify the spending type (impulse or reasonable), and respond accordingly
5. For impulse purchases, provide specific investment alternatives with growth projections
6. For reasonable expenses, acknowledge the necessity and suggest budget allocation
7. If the user is asking about a previous purchase, refer to the context data to provide a relevant response
8. End with a natural follow-up question to continue the conversation when appropriate
9. IMPORTANT: Respond in {getattr(self, 'language', 'fr')} language
"""
                
                # Use self.model instead of self.client.models
                response = self.model.generate_content(
                    contents=[full_prompt],
                    generation_config={
                        "temperature": 0.2,
                        "max_output_tokens": 800
                    }
                )
                
                # Extract the response text
                response_text = response.text
                
                # Extract financial data from the response
                financial_data = self._extract_financial_data(response_text)
                
                return {
                    'is_impulse': financial_data.get('is_impulse', False) if financial_data else False,
                    'amount': financial_data.get('amount', None) if financial_data else None,
                    'category': financial_data.get('category', None) if financial_data else None,
                    'response': response_text,
                    'financial_data': financial_data
                }
                
            except Exception as e:
                logger.error(f"Error in Gemini API call: {str(e)}")
                # Fall back to rule-based analysis only if necessary
                if is_investment_question:
                    return self._handle_investment_question(message)
                else:
                    return self._analyze_message_rule_based(message)
        else:
            # If Gemini is not available, use rule-based analysis
            if is_investment_question:
                return self._handle_investment_question(message)
            else:
                return self._analyze_message_rule_based(message)
    
    def _is_investment_question(self, message: str) -> bool:
        """
        Determine if a message is asking about investments
        
        Args:
            message: The user's message
            
        Returns:
            True if the message is about investments, False otherwise
        """
        message_lower = message.lower()
        
        # Check for investment-related keywords in French and English
        investment_keywords_fr = [
            'investir', 'placement', 'épargne', 'bourse', 'actions', 'obligations',
            'etf', 'fonds', 'rendement', 'intérêt', 'dividende', 'portefeuille',
            'comment investir', 'où investir', 'conseils investissement'
        ]
        
        investment_keywords_en = [
            'invest', 'investment', 'savings', 'stock market', 'stocks', 'bonds',
            'etf', 'fund', 'return', 'interest', 'dividend', 'portfolio',
            'how to invest', 'where to invest', 'investment advice'
        ]
        
        # Check French keywords
        for keyword in investment_keywords_fr:
            if keyword in message_lower:
                return True
                
        # Check English keywords
        for keyword in investment_keywords_en:
            if keyword in message_lower:
                return True
                
        # Check for common investment question patterns
        investment_patterns = [
            r'comment (puis-je |je peux |faire pour |)investir',
            r'où (puis-je |je peux |faire pour |)investir',
            r'conseils (pour |d\'|)investissement',
            r'how (can |do |to |)invest',
            r'where (can |do |to |)invest',
            r'investment advice'
        ]
        
        for pattern in investment_patterns:
            if re.search(pattern, message_lower):
                return True
                
        return False
    
    def _handle_investment_question(self, message: str) -> Dict[str, Any]:
        """
        Handle investment-related questions with detailed advice
        
        Args:
            message: The user's message
            
        Returns:
            Dictionary with response and financial data
        """
        # Extract amount if present
        amount = self._extract_amount(message) or 100  # Default to 100 if no amount specified
        
        # Determine language and personality mode
        language = getattr(self, 'language', 'fr')
        personality_mode = getattr(self, 'personality_mode', 'nice')
        
        # Calculate growth values
        growth_1yr = round(amount * 1.08, 2)
        growth_5yr = round(amount * (1.08**5), 2)
        
        # Generate appropriate response based on language and personality mode
        if language == 'fr':
            if personality_mode == 'nice':
                response = f"""Voici quelques conseils pour investir {amount}€ :

1. **Fonds indiciels ETF** : C'est une excellente option pour les débutants. Vous pouvez investir dans un ETF qui suit un indice comme le S&P 500 ou le MSCI World avec des frais minimes.

2. **Compte d'épargne à haut rendement** : Si vous préférez un risque minimal, un compte d'épargne à haut rendement peut offrir un taux d'intérêt supérieur aux comptes traditionnels.

3. **Plateforme d'investissement fractionnaire** : Des plateformes comme Trade Republic ou Bux vous permettent d'investir de petites sommes dans des actions fractionnées.

4. **Robo-advisors** : Des services comme Yomoni ou Nalo peuvent gérer automatiquement votre portefeuille avec des frais raisonnables.

Avec un investissement de {amount}€ et un rendement annuel moyen de 8%, vous pourriez avoir environ {growth_1yr}€ après un an et {growth_5yr}€ après cinq ans grâce à l'intérêt composé.

Quelle option vous intéresse le plus ?"""
            elif personality_mode == 'funny':
                response = f"""Alors, vous voulez faire travailler vos {amount}€ au lieu de les laisser se prélasser sur votre compte bancaire ? Excellente idée ! 😄

1. **ETFs** : Imaginez que vous achetez un petit morceau de TOUTES les grandes entreprises en même temps ! C'est comme avoir un buffet à volonté financier pour seulement {amount}€. Les frais sont si bas que même votre portefeuille ne les sentira pas passer !

2. **Compte d'épargne à haut rendement** : Pour ceux qui ont le vertige quand leur argent fait des montagnes russes. C'est comme mettre votre argent dans un spa 5 étoiles plutôt que dans un motel bas de gamme !

3. **Actions fractionnées** : Vous avez toujours rêvé de posséder un bout d'Apple ou de Tesla ? Avec {amount}€, vous pouvez acheter 0,0000001% de l'empire d'Elon Musk ! 🚀 Hey, c'est un début !

4. **Robo-advisors** : Comme avoir un conseiller financier en costume-cravate, mais sans avoir à lui offrir de café ni à écouter ses histoires de golf !

Avec vos {amount}€ investis et un rendement de 8% par an, vous aurez {growth_1yr}€ après un an (de quoi vous offrir un café supplémentaire par mois !) et {growth_5yr}€ après cinq ans. Pas mal pour commencer votre empire financier, non ? 💰

Alors, quelle option fait briller vos yeux d'apprenti millionnaire ?"""
            else:  # ironic
                response = f"""Ah, vous voulez investir {amount}€... Quelle somme impressionnante. Voici quelques options, si vous tenez vraiment à vous séparer de cette fortune :

1. **ETFs** : Parce que suivre la masse est toujours une stratégie brillante. Au moins, vous ne serez pas le seul à perdre de l'argent quand le marché s'effondrera.

2. **Compte d'épargne à "haut" rendement** : Avec un taux d'intérêt à peine supérieur à zéro, vous pourrez peut-être vous offrir un chewing-gum supplémentaire dans cinq ans. Quelle perspective excitante.

3. **Actions fractionnées** : Rien de tel que de posséder 0,0000001% d'une entreprise pour se sentir comme un vrai magnat des affaires. Je suis sûr que les PDG vous consulteront pour les grandes décisions.

4. **Robo-advisors** : Parce que confier votre argent à un algorithme est clairement plus rassurant qu'à un humain. Après tout, les robots n'ont jamais causé de problèmes, n'est-ce pas ?

Si tout se passe miraculeusement bien, vos {amount}€ pourraient valoir {growth_1yr}€ dans un an et {growth_5yr}€ dans cinq ans. Ne dépensez pas tout au même endroit.

Alors, quelle option vous semble la moins désastreuse ?"""
        else:  # English
            if personality_mode == 'nice':
                response = f"""Here are some tips for investing ${amount}:

1. **Index ETFs**: This is an excellent option for beginners. You can invest in an ETF that tracks an index like the S&P 500 or MSCI World with minimal fees.

2. **High-yield savings account**: If you prefer minimal risk, a high-yield savings account can offer a higher interest rate than traditional accounts.

3. **Fractional investment platform**: Platforms like Robinhood or M1 Finance allow you to invest small amounts in fractional shares.

4. **Robo-advisors**: Services like Betterment or Wealthfront can automatically manage your portfolio with reasonable fees.

With an investment of ${amount} and an average annual return of 8%, you could have approximately ${growth_1yr} after one year and ${growth_5yr} after five years thanks to compound interest.

Which option interests you the most?"""
            elif personality_mode == 'funny':
                response = f"""So, you want to put your ${amount} to work instead of letting it lounge around in your bank account? Great idea! 😄

1. **ETFs**: Imagine buying a tiny piece of ALL the big companies at once! It's like getting an all-you-can-eat financial buffet for just ${amount}. The fees are so low your wallet won't even feel them!

2. **High-yield savings account**: For those who get dizzy when their money rides roller coasters. It's like putting your money in a 5-star spa instead of a budget motel!

3. **Fractional shares**: Always dreamed of owning a piece of Apple or Tesla? With ${amount}, you can buy 0.0000001% of Elon Musk's empire! 🚀 Hey, it's a start!

4. **Robo-advisors**: Like having a financial advisor in a suit, but without having to offer them coffee or listen to their golf stories!

With your ${amount} invested at an 8% annual return, you'll have ${growth_1yr} after one year (enough for an extra coffee each month!) and ${growth_5yr} after five years. Not bad for starting your financial empire, right? 💰

So, which option makes your apprentice millionaire eyes sparkle?"""
            else:  # ironic
                response = f"""Ah, you want to invest ${amount}... What an impressive sum. Here are some options, if you're really determined to part with this fortune:

1. **ETFs**: Because following the crowd is always a brilliant strategy. At least you won't be the only one losing money when the market crashes.

2. **"High"-yield savings account**: With an interest rate barely above zero, you might be able to afford an extra piece of gum in five years. What an exciting prospect.

3. **Fractional shares**: Nothing like owning 0.0000001% of a company to feel like a real business tycoon. I'm sure the CEOs will consult you on major decisions.

4. **Robo-advisors**: Because trusting your money to an algorithm is clearly more reassuring than a human. After all, robots have never caused any problems, right?

If everything goes miraculously well, your ${amount} could be worth ${growth_1yr} in a year and ${growth_5yr} in five years. Don't spend it all in one place.

So, which option seems the least disastrous to you?"""
        
        return {
            'is_impulse': False,
            'amount': amount,
            'category': 'investments',
            'response': response,
            'financial_data': {
                'type': 'investment',
                'amount': amount,
                'category': 'investments',
                'potential_value_1yr': growth_1yr,
                'potential_value_5yr': growth_5yr
            }
        }
    
    def _analyze_message_rule_based(self, message: str) -> Dict[str, Any]:
        """
        Analyze a message using rule-based methods when Gemini API is not available
        
        Args:
            message: The user's message
            
        Returns:
            Dictionary with analysis results
        """
        logger.info("Using rule-based message analysis")
        
        # Set default language to French if not specified
        language = getattr(self, 'language', 'fr')
        
        # Detect if this is likely an impulse purchase
        is_impulse = self._detect_impulse_purchase(message, language)
        
        # Extract amount if present
        amount = self._extract_amount(message)
        
        # Check for specific keywords in French and English
        message_lower = message.lower()
        
        # Check for shoes/chaussures specifically
        shoe_keywords = ['chaussure', 'chaussures', 'shoe', 'shoes', 'sneaker', 'sneakers', 'basket', 'baskets']
        has_shoes = any(keyword in message_lower for keyword in shoe_keywords)
        
        # Extract category from message
        category = None
        if has_shoes:
            category = 'chaussures' if language == 'fr' else 'shoes'
        else:
            # Try to extract category using regex
            category_match = re.search(r'(?:pour|de|for)\s+(\w+)', message_lower)
            if category_match:
                category = category_match.group(1)
            else:
                # Infer category from message content
                category = self._infer_category(message)
        
        # Force impulse purchase for shoes and certain other categories
        impulse_categories = ['chaussures', 'shoes', 'vêtements', 'clothing', 'électronique', 'electronics']
        if category and any(impulse_cat in category.lower() for impulse_cat in impulse_categories):
            is_impulse = True
        
        # Generate a response based on the analysis
        if is_impulse:
            # Calculate potential investment growth if amount is present
            potential_value_1yr = None
            potential_value_5yr = None
            if amount:
                potential_value_1yr = self._calculate_investment_growth(amount, 1)
                potential_value_5yr = self._calculate_investment_growth(amount, 5)
            
            # Create a more detailed response for impulse purchases
            if language == 'fr':
                if has_shoes:
                    response = f"Je vois que vous avez dépensé {amount}€ pour des chaussures. C'est tentant, mais avez-vous considéré l'impact sur vos finances à long terme?"
                    
                    if amount:
                        response += f"\n\nSi vous aviez investi ces {amount}€ au lieu de les dépenser, vous pourriez avoir environ {potential_value_1yr}€ dans un an et {potential_value_5yr}€ dans cinq ans (avec un rendement annuel de 8%)."
                        response += f"\n\nVoici quelques alternatives d'investissement à considérer:"
                        response += f"\n- Investir dans un ETF qui suit le marché global (rendement moyen de 8% par an)"
                        response += f"\n- Ajouter à votre épargne d'urgence pour plus de sécurité financière"
                        response += f"\n- Contribuer à un plan d'épargne retraite pour bénéficier d'avantages fiscaux"
                else:
                    response = f"Je vois que vous avez dépensé {amount}€. Était-ce un achat planifié ou plutôt impulsif?"
                    
                    if amount:
                        response += f"\n\nSi c'était impulsif, sachez que si vous aviez investi ces {amount}€, vous pourriez avoir environ {potential_value_1yr}€ dans un an et {potential_value_5yr}€ dans cinq ans (avec un rendement annuel de 8%)."
            else:  # English
                if has_shoes:
                    response = f"I see you spent ${amount} on shoes. It's tempting, but have you considered the long-term impact on your finances?"
                    
                    if amount:
                        response += f"\n\nIf you had invested this ${amount} instead of spending it, you could have approximately ${potential_value_1yr} in one year and ${potential_value_5yr} in five years (at an 8% annual return)."
                        response += f"\n\nHere are some investment alternatives to consider:"
                        response += f"\n- Invest in an ETF that tracks the global market (average return of 8% per year)"
                        response += f"\n- Add to your emergency fund for more financial security"
                        response += f"\n- Contribute to a retirement savings plan for tax benefits"
                else:
                    response = f"I see you spent ${amount}. Was this a planned purchase or more of an impulse buy?"
                    
                    if amount:
                        response += f"\n\nIf it was impulsive, know that if you had invested this ${amount}, you could have approximately ${potential_value_1yr} in one year and ${potential_value_5yr} in five years (at an 8% annual return)."
            
            return {
                'is_impulse': True,
                'amount': amount,
                'category': category,
                'response': response,
                'financial_data': {
                    'type': 'impulse',
                    'amount': amount,
                    'category': category,
                    'potential_value_1yr': potential_value_1yr,
                    'potential_value_5yr': potential_value_5yr
                } if amount else None
            }
        else:
            # For non-impulse purchases, create a budget-focused response
            if language == 'fr':
                if category:
                    response = f"J'ai noté votre dépense de {amount}€ pour {category}. Voulez-vous que je l'ajoute à votre budget mensuel?"
                else:
                    response = f"J'ai noté votre dépense de {amount}€. Dans quelle catégorie de budget devrais-je la classer?"
            else:  # English
                if category:
                    response = f"I've noted your expense of ${amount} for {category}. Would you like me to add it to your monthly budget?"
                else:
                    response = f"I've noted your expense of ${amount}. Which budget category should I classify it under?"
            
            return {
                'is_impulse': False,
                'amount': amount,
                'category': category,
                'response': response,
                'financial_data': {
                    'type': 'reasonable',
                    'amount': amount,
                    'category': category,
                    'budget_allocation': True
                } if amount else None
            }
    
    def generate_investment_advice(self, amount: float, category: str) -> Dict[str, Any]:
        """Generate investment alternatives for a specific amount"""
        try:
            logger.info(f"Generating investment advice for {self.currency_symbols[self.preferred_currency]}{amount} in category: {category}")
            
            prompt = f"""
            The user is considering spending {self.currency_symbols[self.preferred_currency]}{amount} on {category}. 
            Provide 2-3 investment alternatives with potential 1-year and 5-year growth projections.
            Format the response conversationally but include specific numbers.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.3
                ),
                contents=[prompt]
            )
            
            return {"response": response.text}
            
        except Exception as e:
            logger.error(f"Error generating investment advice: {str(e)}", exc_info=True)
            return {"response": "I'm sorry, I encountered an error generating investment advice. Please try again."}
    
    def generate_budget_advice(self, amount: float, category: str) -> Dict[str, Any]:
        """Generate budgeting advice for reasonable spending"""
        logger.info(f"Generating budget advice for {self.currency_symbols[self.preferred_currency]}{amount} in category: {category}")
        
        # Translate category if needed
        translated_category = self._translate_category(category, self.language)
        
        # Prepare a prompt for the model
        prompt = f"""
The user is spending {self.currency_symbols[self.preferred_currency]}{amount} on {translated_category}, which appears to be a reasonable expense.
Generate a very brief response acknowledging this expense has been added to their budget.
If in sarcastic mode, add a touch of dry humor.
"""
        
        result = {
            "financialData": {
                "type": "reasonable",
                "amount": amount,
                "category": category,
                "budget_allocation": True
            }
        }
        
        try:
            # For reasonable expenses, keep responses very brief
            if self.language == 'fr':
                if self.personality_mode == "nice":
                    result["response"] = f"J'ai ajouté {self.currency_symbols[self.preferred_currency]}{amount} pour {translated_category} à votre budget."
                else:  # sarcastic mode
                    sarcastic_responses = [
                        f"Bon, j'ai ajouté vos {self.currency_symbols[self.preferred_currency]}{amount} de dépense {translated_category} à votre budget. Content maintenant ?",
                        f"{self.currency_symbols[self.preferred_currency]}{amount} pour {translated_category} ? Ajouté à votre budget. Votre comptable serait si fier.",
                        f"Encore {self.currency_symbols[self.preferred_currency]}{amount} pour {translated_category} ? Ajouté à votre budget. Au moins ce n'est pas un autre achat impulsif.",
                        f"Budget mis à jour : {self.currency_symbols[self.preferred_currency]}{amount} pour {translated_category}. Votre futur vous envoie ses salutations.",
                        f"{self.currency_symbols[self.preferred_currency]}{amount} pour {translated_category} - nécessaire, je suppose. Ajouté à votre budget."
                    ]
                    import random
                    result["response"] = random.choice(sarcastic_responses)
            else:  # English
                if self.personality_mode == "nice":
                    result["response"] = f"Added {self.currency_symbols[self.preferred_currency]}{amount} for {category} to your budget."
                else:  # sarcastic mode
                    sarcastic_responses = [
                        f"Fine, I've added your {self.currency_symbols[self.preferred_currency]}{amount} {category} expense to your budget. Happy now?",
                        f"{self.currency_symbols[self.preferred_currency]}{amount} on {category}? Added to your budget. Your accountant would be so proud.",
                        f"Another {self.currency_symbols[self.preferred_currency]}{amount} for {category}? Added to your budget. At least it's not another impulse buy.",
                        f"Budget updated: {self.currency_symbols[self.preferred_currency]}{amount} for {category}. Your future self sends their regards.",
                        f"{self.currency_symbols[self.preferred_currency]}{amount} for {category} - necessary, I suppose. Added to your budget."
                    ]
                    import random
                    result["response"] = random.choice(sarcastic_responses)
                
            return result
        except Exception as e:
            logger.error(f"Error generating budget advice: {e}")
            return {"response": f"I've added your {category} expense of {self.currency_symbols[self.preferred_currency]}{amount} to your budget."}
    
    def _extract_financial_data(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract financial data JSON from the response text"""
        # Look for JSON pattern in the text
        json_pattern = r'```json\s*({.*?})\s*```|{[\s\S]*?"financialData"[\s\S]*?}'
        match = re.search(json_pattern, text, re.DOTALL)
        
        if match:
            try:
                json_str = match.group(1) if match.group(1) else match.group(0)
                # Clean up the JSON string
                json_str = re.sub(r'```json|```', '', json_str).strip()
                data = json.loads(json_str)
                
                # If the JSON contains a financialData key, return just that
                if "financialData" in data:
                    return data["financialData"]
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from response: {str(e)}")
                # Try a more aggressive approach to extract JSON
                try:
                    # Find anything that looks like a JSON object
                    potential_json = re.search(r'{[^{}]*"amount"[^{}]*}', text)
                    if potential_json:
                        # Replace single quotes with double quotes and try again
                        fixed_json = potential_json.group(0).replace("'", '"')
                        return json.loads(fixed_json)
                except Exception:
                    logger.error("Failed aggressive JSON extraction attempt")
                return None
        
        # If no JSON found, try to extract financial information directly from text
        return self._extract_financial_info_from_text(text)
    
    def _extract_financial_info_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract financial information directly from text when JSON extraction fails"""
        # Look for pound amounts
        amount_pattern = r'£(\d+(?:\.\d+)?)'
        amount_matches = re.findall(amount_pattern, text)
        
        if amount_matches:
            try:
                # Use the first amount found
                amount = float(amount_matches[0])
                
                # Look for common categories
                categories = ["clothing", "electronics", "gadget", "food", "dining", "travel", 
                             "entertainment", "subscription", "shoes", "accessory", "home", "furniture",
                             "medical", "healthcare", "groceries", "utilities", "education", "childcare"]
                
                category = None
                for cat in categories:
                    if cat in text.lower() or cat + "s" in text.lower():
                        category = cat
                        break
                
                # Determine spending type
                spending_type = self._classify_spending_type(text, category or "general")
                
                if spending_type == "impulse":
                    # Calculate growth values
                    one_year = amount * 1.08
                    five_year = amount * (1.08 ** 5)
                    
                    return {
                        "type": "impulse",
                        "amount": amount,
                        "category": category or "general",
                        "potential_value_1yr": one_year,
                        "potential_value_5yr": five_year
                    }
                else:
                    return {
                        "type": "reasonable",
                        "amount": amount,
                        "category": category or "general",
                        "budget_allocation": True
                    }
            except Exception as e:
                logger.error(f"Error extracting financial info from text: {str(e)}")
        
        return None
    
    def _ensure_complete_financial_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure the financial data has all required fields with reasonable values"""
        if not data:
            return {}
            
        # Make a copy to avoid modifying the original
        result = dict(data)
        
        # Ensure type field (default to impulse if not specified)
        if 'type' not in result:
            result['type'] = self._classify_spending_type("", result.get('category', 'general'))
            
        # Ensure amount is present and valid
        if 'amount' not in result or not isinstance(result['amount'], (int, float)) or result['amount'] <= 0:
            # If invalid amount, we can't proceed
            logger.warning("Invalid or missing amount in financial data")
            return {}
            
        # Ensure category
        if 'category' not in result or not result['category']:
            result['category'] = 'general'
            
        # Add appropriate fields based on spending type
        if result['type'] == 'impulse':
            # Calculate growth values if missing
            amount = float(result['amount'])
            if 'potential_value_1yr' not in result or not isinstance(result['potential_value_1yr'], (int, float)):
                result['potential_value_1yr'] = round(amount * 1.08, 2)
                
            if 'potential_value_5yr' not in result or not isinstance(result['potential_value_5yr'], (int, float)):
                result['potential_value_5yr'] = round(amount * (1.08 ** 5), 2)
        elif result['type'] == 'reasonable':
            # Add budget allocation flag if missing
            if 'budget_allocation' not in result:
                result['budget_allocation'] = True
            
        return result
    
    def _classify_spending_type(self, message: str, category: str) -> str:
        """Classify spending as either 'impulse' or 'reasonable' based on message and category"""
        # List of categories that are almost always reasonable
        reasonable_categories = [
            'medical', 'healthcare', 'doctor', 'medicine', 'prescription',
            'groceries', 'grocery', 'food essentials', 'essential food',
            'rent', 'mortgage', 'housing', 'utilities', 'bills', 'electricity', 'water', 'gas',
            'transportation', 'commute', 'fuel', 'public transport',
            'education', 'tuition', 'school', 'books', 'supplies',
            'childcare', 'daycare'
        ]
        
        # Check if category is in reasonable categories
        category = category.lower()
        if any(reasonable_cat in category for reasonable_cat in reasonable_categories):
            return "reasonable"
            
        # Check message for reasonable spending indicators
        message = message.lower()
        if any(term in message for term in reasonable_categories):
            return "reasonable"
            
        # Check for phrases indicating necessity
        necessity_phrases = [
            'need', 'necessary', 'essential', 'required', 'have to', 'must', 
            'important', 'critical', 'vital', 'emergency', 'urgent'
        ]
        
        if any(phrase in message for phrase in necessity_phrases):
            return "reasonable"
            
        # Check for impulse indicators
        impulse_phrases = [
            'want', 'impulse', 'splurge', 'treat myself', 'tempted', 'thinking of buying',
            'just saw', 'cool', 'awesome', 'fancy', 'luxury', 'designer', 'latest'
        ]
        
        if any(phrase in message for phrase in impulse_phrases):
            return "impulse"
            
        # Default to impulse if we can't determine (erring on the side of encouraging mindful spending)
        return "impulse"
    
    def _infer_category(self, message: str) -> str:
        """Infer spending category from the message"""
        message = message.lower()
        
        category_keywords = {
            'electronics': ['phone', 'laptop', 'computer', 'tablet', 'gadget', 'tech', 'electronic'],
            'clothing': ['shirt', 'dress', 'pants', 'clothes', 'jacket', 'fashion'],
            'shoes': ['shoes', 'sneakers', 'boots', 'footwear'],
            'accessories': ['watch', 'jewelry', 'bag', 'purse', 'accessory'],
            'home': ['furniture', 'decor', 'house', 'apartment', 'home'],
            'entertainment': ['game', 'movie', 'subscription', 'streaming', 'concert', 'ticket'],
            'dining': ['restaurant', 'dinner', 'lunch', 'food', 'eat out'],
            'travel': ['vacation', 'trip', 'flight', 'hotel', 'travel'],
            'groceries': ['grocery', 'groceries', 'supermarket', 'food shopping'],
            'medical': ['doctor', 'hospital', 'medicine', 'prescription', 'healthcare', 'medical'],
            'utilities': ['bill', 'utility', 'electricity', 'water', 'gas', 'internet'],
            'education': ['tuition', 'school', 'course', 'class', 'book', 'education'],
            'childcare': ['daycare', 'babysitter', 'childcare', 'children']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in message for keyword in keywords):
                return category
                
        return 'general'
    
    def _clean_response_text(self, text: str) -> str:
        """Remove JSON and other technical content from the response text"""
        # Remove JSON blocks
        text = re.sub(r'```json.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'{[\s\S]*?"financialData"[\s\S]*?}', '', text)
        
        # Remove any remaining JSON-like structures
        text = re.sub(r'{.*}', '', text, flags=re.DOTALL)
        
        # Clean up extra whitespace and newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        
        return text
        
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
            
            # Analyze the message and get a response
            result = self.analyze_message(message, conversation_history, context_data)
            
            # Return the response text
            return result.get('response', 'Sorry, I could not generate a response.')
        except Exception as e:
            logger.error(f"Error getting response from Gemini: {str(e)}")
            
            # Fallback responses based on language
            if language == 'fr':
                return "Désolé, je n'ai pas pu traiter votre demande. Veuillez réessayer."
            else:
                return "Sorry, I couldn't process your request. Please try again."

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