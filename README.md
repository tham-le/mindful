# MindfulWealth

MindfulWealth is a personal finance application designed to help users make mindful spending decisions by intercepting impulse purchases and suggesting investment alternatives. The application provides a comprehensive dashboard for financial tracking and AI-powered chat assistance.

## Features

- **Smart Dashboard**: View your financial health at a glance with portfolio allocation, recent transactions, goal progress, and actionable insights.
- **AI-Powered Chat**: Interact with an AI assistant that understands your financial situation and provides personalized advice.
- **Impulse Purchase Interception**: Identify potential impulse purchases and see how that money could grow if invested instead.
- **Financial Goal Tracking**: Set and monitor progress towards your financial goals.
- **Portfolio Management**: Track your investments and asset allocation.

## Project Structure

The project consists of two main components:

1. **Backend (Python/Flask)**
   - API endpoints for financial data
   - Gemini AI integration for chat functionality
   - Database models and services

2. **Frontend (React)**
   - Modern, responsive UI
   - Dashboard components
   - Chat interface
   - Financial visualization

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/mindfulwealth.git
   cd mindfulwealth
   ```

2. Set up the backend:

   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:

   ```
   cd ../mindfulwealth-react
   npm install
   ```

4. Configure environment variables:
   - Create a `.env` file in the backend directory with your Gemini API key:

     ```
     GEMINI_API_KEY=your_api_key_here
     ```

### Running the Application

1. Start the backend server:

   ```
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python app.py
   ```

2. Start the frontend development server:

   ```
   cd ../mindfulwealth-react
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Testing

The application includes comprehensive test suites for both backend and frontend components.

### Running Tests

Use the provided test runner script to run all tests:

```
./run_tests.sh
```

This script will:

- Run all backend tests using pytest
- Run all frontend tests using Jest
- Provide a summary of test results

### Test Structure

- **Backend Tests**:
  - API endpoint tests
  - Gemini service tests
  - Database model tests

- **Frontend Tests**:
  - Component rendering tests
  - API integration tests
  - User interaction tests

## API Documentation

### Dashboard API

- `GET /api/dashboard`: Returns comprehensive dashboard data including financial summary, portfolio allocation, and insights.
- `GET /api/goals`: Returns the user's financial goals and progress.
- `GET /api/portfolio`: Returns the user's investment portfolio details.
- `GET /api/activity`: Returns recent financial activities and transactions.
- `GET /api/insights`: Returns personalized financial insights and recommendations.

### Chat API

- `POST /api/chat`: Sends a message to the AI assistant and returns a response.
  - Request body: `{ "message": "string" }`
  - Response: `{ "response": "string", "financial_data": object }`

- `POST /api/personality`: Sets the personality mode for the AI assistant.
  - Request body: `{ "mode": "string" }`
  - Response: `{ "success": boolean, "mode": "string" }`

### Transaction API

- `GET /api/transactions`: Returns the user's transactions.
- `POST /api/transactions`: Adds a new transaction.
  - Request body: `{ "amount": number, "category": "string", "description": "string", "date": "string" }`

### Budget API

- `GET /api/budget`: Returns the user's budget information.
- `POST /api/budget`: Creates or updates a budget.
  - Request body: `{ "category": "string", "amount": number }`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Gemini AI](https://ai.google.dev/) for powering the chat assistant
- [React](https://reactjs.org/) for the frontend framework
- [Flask](https://flask.palletsprojects.com/) for the backend framework
- [Chart.js](https://www.chartjs.org/) for data visualization
- [Heroicons](https://heroicons.com/) for UI icons

## Documentation

For detailed documentation about the application, please refer to the [Documentation Index](docs/README.md).
