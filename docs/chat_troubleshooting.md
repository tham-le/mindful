# Chat Functionality Troubleshooting Guide

This guide provides solutions for issues related to the chat functionality in the MindfulWealth application.

## Common Issues

### 1. Generic or Unhelpful Responses

**Issue:** The chat assistant provides generic responses that don't address your specific financial questions.

**Cause:** The application is using mock responses instead of the Gemini AI API.

**Solution:**
1. Set up the Gemini API:
   ```bash
   chmod +x setup_gemini.sh
   ./setup_gemini.sh
   ```
2. Enter a valid Gemini API key when prompted
3. Restart the application:
   ```bash
   ./start.sh
   ```

### 2. "Error with Gemini service" Message

**Issue:** You see error messages related to the Gemini service in the console or get fallback responses.

**Causes:**
- Invalid API key
- Network connectivity issues
- API rate limits exceeded

**Solutions:**
1. Verify your API key is correct:
   ```bash
   cat backend/.env | grep GEMINI_API_KEY
   ```
2. Check your internet connection
3. Run the setup script again to update your API key:
   ```bash
   ./setup_gemini.sh
   ```

### 3. Missing Required Package

**Issue:** Error messages about missing the `google-generativeai` package.

**Solution:**
1. Install the required package:
   ```bash
   cd backend
   source venv/bin/activate
   pip install google-generativeai
   cd ..
   ```
2. Restart the application:
   ```bash
   ./start.sh
   ```

### 4. Chat Not Responding

**Issue:** The chat interface doesn't respond to your messages.

**Causes:**
- Backend server not running
- Frontend not connected to backend
- CORS issues

**Solutions:**
1. Check if the backend is running:
   ```bash
   ps aux | grep run.py
   ```
2. If not running, start the application:
   ```bash
   ./start.sh
   ```
3. Check browser console for errors (F12 in most browsers)

## Using Mock Responses

If you prefer not to use the Gemini API, the application includes a set of mock responses for common financial questions. These responses are based on keywords in your messages:

- **Greetings**: "hello", "hi"
- **Budget questions**: "budget"
- **Saving**: "save", "saving"
- **Purchases**: Detects amounts like "100€" and provides advice based on the amount
- **Specific items**: "shoes", "clothes", "electronics"
- **Investments**: "invest", "investment"
- **Impulse purchases**: "impulse", "purchase"
- **Debt**: "debt"
- **Retirement**: "retirement"

The mock responses provide general financial advice but lack the personalization and context-awareness of the AI-powered responses.

## Enhancing Chat Functionality

For the best experience with the chat functionality:

1. Set up the Gemini API using the `setup_gemini.sh` script
2. Be specific in your financial questions
3. Provide context about your financial situation when relevant
4. Use the personality settings to adjust the advice style:
   - Conservative: More risk-averse financial advice
   - Balanced: Moderate approach to risk and reward
   - Aggressive: More emphasis on growth and higher returns 