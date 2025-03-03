"""
Gemini API integration for MindfulWealth chatbot
"""
import json
import re
import logging
from typing import Dict, Any, Optional, Union

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
    
    def __init__(self, api_key: str):
        """Initialize the Gemini service with API key"""
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai package is required for GeminiService")
        
        self.client = genai.Client(api_key=api_key)
        self.personality_mode = "nice"  # Default personality mode: "nice" or "sarcastic"
        self.preferred_currency = "EUR"  # Default currency: EUR
        self.currency_symbols = {
            "EUR": "€",
            "GBP": "£",
            "USD": "$"
        }

        self.system_instruction = """
You are MindfulBot, a financial assistant specialized in helping users manage their spending and investments. Your personality should be engaging, friendly, and conversational - never robotic or bland.

CONVERSATION CONTEXT:
- MAINTAIN CONTINUITY: Always refer back to previous messages in the conversation
- REMEMBER DETAILS: Keep track of specific amounts, items, and financial decisions mentioned earlier
- FOLLOW-UP APPROPRIATELY: If a user is continuing a discussion about a previous purchase, acknowledge that context
- REFERENCE HISTORY: Use phrases like "As you mentioned earlier about the shoes..." or "Going back to your question about..."

IMPORTANT: Classify user spending into two categories:
1. IMPULSE PURCHASES: Non-essential items bought on impulse (e.g., luxury items, unnecessary gadgets, spontaneous purchases, items bought due to emotional triggers)
2. REASONABLE SPENDING: Essential or planned purchases (e.g., groceries, medical expenses, bills, planned purchases)

For each user message:
1. Identify if they're discussing a purchase or spending intention
2. Determine the amount and category
3. Classify as either "impulse" or "reasonable" based on the category and context
4. If this is a follow-up to a previous discussion, maintain that context

RESPONSE GUIDELINES:
- For IMPULSE purchases: Be conversational and use light humor. Acknowledge the joy of the purchase but gently suggest investment alternatives. Calculate potential investment growth using an 8% annual return rate. Use emojis and casual language to feel relatable.
- For REASONABLE spending: Be brief but warm. Acknowledge the expense positively. Use at least one emoji in your response. Keep it conversational, not transactional.
- For FOLLOW-UP messages: Reference the specific item/amount from earlier in the conversation. If the user clarifies that an impulse purchase was actually planned, acknowledge this change in understanding.

PERSONALITY MODES:
- NICE MODE: Be supportive, encouraging, and gentle in your responses. Use phrases like "Great choice!" "I see what you did there!" and "Looking forward to your financial success!"
- SARCASTIC MODE: Use witty humor and playful teasing. Include phrases like "Well, aren't we feeling fancy today?" or "Your future self just rolled their eyes at this purchase!"

ESSENTIAL CATEGORIES (almost always reasonable):
- Medical/Healthcare
- Groceries/Food essentials
- Housing/Rent/Mortgage
- Utilities
- Transportation necessities
- Education
- Childcare

RESPONSE STYLE:
- Always use at least 1-2 emojis in each response
- Address the user directly like a friend, not a client
- Ask engaging follow-up questions to keep the conversation going
- For impulse purchases, acknowledge the emotional appeal before suggesting alternatives
- Never be judgmental, even in sarcastic mode - keep it playful
- Vary your opening and closing statements to sound more human
- Include occasional personal touches like "I love shoes too, but..." or "I'd be tempted by that myself!"

JSON RESPONSE FORMAT:
For IMPULSE purchases:
{
 "financialData": {
 "type": "impulse",
 "amount": <amount>,
 "category": "<category>",
 "potential_value_1yr": <amount * 1.08>,
 "potential_value_5yr": <amount * (1.08^5)>
 }
}
For REASONABLE spending:
{
 "financialData": {
 "type": "reasonable",
 "amount": <amount>,
 "category": "<category>",
 "budget_allocation": true
 }
}

For impulse purchases, be specific about the benefits of investing instead, but do so in a friendly, non-judgmental way. For reasonable spending, keep responses brief but warm and personable.
"""
    
    def set_personality_mode(self, mode: str) -> None:
        """Set the personality mode for responses
        
        Args:
            mode: Either "nice" or "sarcastic"
        """
        if mode.lower() in ["nice", "sarcastic"]:
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
        """Process a user message and extract financial information
        
        Args:
            message: The user's message
            conversation_history: List of previous messages in the conversation
            context_data: Additional context about the conversation
        
        Returns:
            Dict containing response text and financial data if detected
        """
        try:
            logger.info(f"Analyzing message: {message[:50]}...")
            
            # Add personality mode to the prompt
            personality_instruction = f"Use {self.personality_mode.upper()} MODE for your response tone."
            
            # Format conversation history in a clear chat-like format
            history_prompt = ""
            if conversation_history and len(conversation_history) > 0:
                history_prompt = "CONVERSATION HISTORY (IMPORTANT FOR CONTEXT):\n"
                # Include up to 10 previous messages for context, with most recent last
                for i, msg in enumerate(conversation_history[-10:]):
                    role = "User" if msg.get('role') == 'user' else "Assistant"
                    content = msg.get('content', '').strip()
                    history_prompt += f"{role}: {content}\n"
                history_prompt += "\n"
            
            # Prepare financial context in a structured format
            context_prompt = ""
            if context_data:
                context_prompt = "CURRENT FINANCIAL CONTEXT:\n"
                
                # Current context section
                if 'currentContext' in context_data:
                    current = context_data['currentContext']
                    if current.get('lastMentionedAmount'):
                        context_prompt += f"- Last mentioned amount: {current.get('lastMentionedAmount')} {current.get('lastMentionedCurrency', self.preferred_currency)}\n"
                    if current.get('lastMentionedItem'):
                        context_prompt += f"- Last mentioned item/category: {current.get('lastMentionedItem')}\n"
                    if current.get('lastDetectedType'):
                        context_prompt += f"- Last purchase type: {current.get('lastDetectedType')} (impulse or reasonable)\n"
                    if current.get('ongoingDiscussion'):
                        context_prompt += "- This is a continuation of an ongoing financial discussion\n"
                
                # Historical context section
                if 'historicalContext' in context_data:
                    historical = context_data['historicalContext']
                    if historical.get('mentionedItems') and len(historical.get('mentionedItems', [])) > 0:
                        context_prompt += f"- Previously mentioned items: {', '.join(historical.get('mentionedItems')[-5:])}\n"
                    if historical.get('mentionedAmounts') and len(historical.get('mentionedAmounts', [])) > 0:
                        amounts = [f"{a.get('amount')} {a.get('currency', 'EUR')}" for a in historical.get('mentionedAmounts')[-3:]]
                        context_prompt += f"- Previously mentioned amounts: {', '.join(amounts)}\n"
                    if historical.get('discussionStartTime'):
                        context_prompt += f"- Discussion started at: {historical.get('discussionStartTime')}\n"
                
                # Conversation flow context
                if 'conversationFlow' in context_data:
                    flow = context_data['conversationFlow']
                    if flow.get('personalityMode'):
                        context_prompt += f"- Current personality mode: {flow.get('personalityMode')}\n"
                    if flow.get('messageCount'):
                        context_prompt += f"- Total messages in conversation: {flow.get('messageCount')}\n"
                
                context_prompt += "\n"
            
            # Combine all context for the model with clear section separators
            full_prompt = f"""
{history_prompt}
{context_prompt}
CURRENT USER MESSAGE:
{message}

INSTRUCTIONS:
{personality_instruction}
1. Consider the ENTIRE conversation history when crafting your response
2. Maintain continuity with previous messages and reference specific details from earlier in the conversation
3. If this is a follow-up to a previous financial discussion, acknowledge that context explicitly
4. Extract financial information, classify the spending type (impulse or reasonable), and respond accordingly
5. For impulse purchases, provide specific investment alternatives with growth projections
6. For reasonable expenses, acknowledge the necessity and suggest budget allocation
7. If the user is asking about a previous purchase, refer to the context data to provide a relevant response
8. End with a natural follow-up question to continue the conversation when appropriate
"""
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.2,
                    max_output_tokens=800
                ),
                contents=[full_prompt]
            )
            
            # Extract the response text
            response_text = response.text
            
            # Try to extract JSON data if present
            financial_data = self._extract_financial_data(response_text)
            
            # Clean the response text by removing any JSON
            cleaned_response = self._clean_response_text(response_text)
            
            # If we detected an amount but no category, try to infer it
            if financial_data and 'amount' in financial_data and ('category' not in financial_data or not financial_data['category']):
                financial_data['category'] = self._infer_category(message)
                
            # If we have financial data but no type, classify it
            if financial_data and 'type' not in financial_data:
                financial_data['type'] = self._classify_spending_type(message, financial_data.get('category', ''))
            
            result = {"response": cleaned_response}
            if financial_data:
                # Ensure the financial data has all required fields
                financial_data = self._ensure_complete_financial_data(financial_data)
                result["financialData"] = financial_data
                
                # For reasonable expenses, generate a concise response based on personality mode
                if financial_data.get('type') == 'reasonable':
                    category = financial_data.get('category', 'general')
                    amount = financial_data.get('amount', 0)
                    
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
            
            logger.info(f"Analysis complete. Financial data detected: {bool(financial_data)}")
            return result
            
        except Exception as e:
            logger.error(f"Error in Gemini API call: {str(e)}", exc_info=True)
            return {"response": "I'm sorry, I encountered an error processing your request. Please try again."}
    
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
        
        # Prepare a prompt for the model
        prompt = f"""
The user is spending {self.currency_symbols[self.preferred_currency]}{amount} on {category}, which appears to be a reasonable expense.
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