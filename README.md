# MindfulWealth Chatbot

A financial chatbot that helps transform shopping impulses into investment growth opportunities.

## Project Overview

MindfulWealth analyzes user messages about spending intentions or completed purchases, detects impulsive buying patterns, and provides guidance to redirect spending toward investments. The application features both a conversational interface and data visualization dashboard.

## Features

- **Conversational Interface**: Natural language processing for financial queries
- **Impulse Detection**: Recognition of impulsive buying patterns through text analysis
- **Investment Redirection**: Personalized investment suggestions based on spending patterns
- **Financial Dashboard**: Visualize budget, spending, and potential investment growth
- **Robust Error Handling**: Graceful handling of connection issues and API errors
- **Smart Spending Classification**: Automatically distinguishes between impulse purchases and necessary expenses
- **Budget Integration**: Necessary expenses are automatically added to your monthly budget
- **Category Detection**: Automatic categorization of spending intentions
- **Personality Modes**: Choose between "Nice" and "Sarcastic" response styles
- **Currency Selection**: Switch between EUR, GBP, and USD with a simple toggle (default: EUR)
- **Mobile-Friendly Design**: Responsive layout that works well on all devices

## How It Works

MindfulWealth uses advanced natural language processing to analyze your spending messages:

1. **Spending Classification**: The AI determines if your purchase is:
   - **Impulse Purchase**: Non-essential items bought on impulse (e.g., luxury items, gadgets)
   - **Reasonable Expense**: Essential or planned purchases (e.g., groceries, medical expenses)

2. **Tailored Responses**:
   - For impulse purchases: Provides investment alternatives and growth projections
   - For reasonable expenses: Acknowledges the necessity and adds it to your monthly budget

3. **Personality Modes**:
   - **Nice Mode**: Supportive, encouraging, and gentle responses
   - **Sarcastic Mode**: Witty, humorous responses with a touch of sarcasm

4. **Currency Handling**:
   - Choose your preferred currency (EUR, GBP, USD) from the header or footer
   - Automatically detects and converts currencies in user messages
   - All financial calculations are standardized to your selected currency

5. **Essential Categories**: Automatically recognizes essential spending categories like:
   - Medical/Healthcare
   - Groceries/Food essentials
   - Housing/Rent/Mortgage
   - Utilities
   - Transportation necessities
   - Education
   - Childcare

## Tech Stack

### Frontend
- Vue.js 3 with Composition API
- Vite as the build tool
- Chart.js for data visualization

### Backend
- Flask RESTful API
- SQLite database (for MVP)
- Google Gemini 2.0 Flash for natural language processing

## Setup Instructions

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- Google Gemini API key (optional for development)

### Frontend Setup
```bash
# Navigate to the frontend directory
cd mindfulwealth

# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
# GEMINI_API_KEY=your_api_key_here

# Start the Flask server
python app.py
```

### Quick Start
For convenience, you can use the provided start script to launch both servers:

```bash
# Make the script executable
chmod +x start.sh

# Run the script
./start.sh
```

## Testing

### Backend API Testing
A test script is provided to verify the backend API functionality:

```bash
# Make sure the backend server is running
cd backend
./test_api.py
```

This will test all API endpoints and provide a summary of results.

## Usage

1. Start both the frontend and backend servers
2. Open your browser to http://localhost:5173
3. Select your preferred currency using the currency selector in the header or footer
4. Toggle between "Nice" and "Sarcastic" personality modes using the switch in the chat header
5. Interact with the chatbot by typing messages about purchases
6. View your financial data in the dashboard
7. Track redirected impulse purchases in the Impulse Tracker

## Example Interactions

### Impulse Purchase (Nice Mode)
```
User: "I'm thinking of buying a new smartwatch for €299"
Bot: "That sounds like an impulse purchase. If you invested €299 instead, it could grow to €323 in one year and €439 in five years at an 8% annual return."
```

### Reasonable Expense (Nice Mode)
```
User: "I need to pay €120 for my prescription medication"
Bot: "Added €120 for medical to your budget."
```

### Reasonable Expense (Sarcastic Mode)
```
User: "I bought 200 dollars of groceries"
Bot: "€184 on groceries? Added to your budget. Your accountant would be so proud."
```

### Multi-Currency Support
```
User: "I spent 50 pounds on dinner"
Bot: "Added €59 for dining to your budget."
```

## Development

### Frontend Structure
- `src/components/ChatInterface.vue`: Chat input and message display
- `src/components/FinancialDashboard.vue`: Budget visualization
- `src/components/ImpulsePurchaseTracker.vue`: Tracked impulse redirections
- `src/services/api.js`: API communication layer

### Backend Structure
- `app.py`: Main Flask application
- `models.py`: Database models
- `services/gemini_service.py`: Gemini API integration
- `test_api.py`: API testing script

## Deployment

### Frontend Deployment
```bash
# Build for production
npm run build

# The dist folder can be deployed to any static hosting service
```

### Backend Deployment
```bash
# Install gunicorn (included in requirements.txt)
# Start with gunicorn
gunicorn app:app
```

## Future Enhancements

- User authentication and personalized profiles
- More sophisticated impulse detection algorithms
- Expanded investment options and risk assessment
- Mobile application version
- Integration with real financial data providers
- Personalized investment recommendations based on risk profile
- Additional personality modes and response styles

## Security Notes

- Never commit your `.env` file with API keys to version control
- The `.env.example` file provides a template for required environment variables
- For production, use environment variables set on the server rather than `.env` files

## License

MIT 