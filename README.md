# MindfulWealth - Financial Wellness Assistant

MindfulWealth is a personal financial wellness assistant that helps users manage their finances, track spending, set budgets, and make mindful financial decisions.

## Features

- **User Authentication**: Register, login, or use a demo account without registration
- **Financial Dashboard**: View your financial overview, including spending, budget, and savings
- **Transaction Tracking**: Record and categorize your financial transactions
- **Budget Management**: Set and track budgets by category
- **Impulse Purchase Redirection**: Save money by redirecting impulse purchases to savings
- **Chat Interface**: Interact with the financial assistant through a chat interface
- **Personalization**: Choose between different personality modes for the assistant

## Tech Stack

- **Frontend**: React, Tailwind CSS, Chart.js
- **Backend**: Flask, SQLAlchemy, SQLite
- **Authentication**: JWT (JSON Web Tokens)

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+
- python3-venv package (for virtual environment)

On Ubuntu/Debian, you can install the required packages with:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mindfulwealth.git
   cd mindfulwealth
   ```

2. Run the setup script to install dependencies:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   This script will:
   - Create a Python virtual environment
   - Install backend dependencies
   - Run database migrations
   - Initialize the database
   - Install frontend dependencies

3. Start the application:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

   This script will:
   - Activate the Python virtual environment
   - Start the backend server
   - Start the frontend server

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Setting Up AI-Powered Financial Advice

By default, the application uses mock responses for the chat functionality. To enable AI-powered financial advice using Google's Gemini API:

1. Get a free Gemini API key from [Google AI Studio](https://ai.google.dev/)

2. Run the Gemini setup script:
   ```bash
   chmod +x setup_gemini.sh
   ./setup_gemini.sh
   ```

3. Follow the prompts to enter your API key

4. Restart the application:
   ```bash
   ./start.sh
   ```

### Database Issues

If you encounter database-related errors (such as missing columns or tables), you can fix them by running:

```bash
chmod +x fix_database.sh
./fix_database.sh
```

This script will:
1. Back up your current database
2. Run the migration script to update the schema
3. Initialize the database with the updated schema

For a complete summary of how we addressed a specific database issue, see [Database Fix Summary](docs/database_fix_summary.md).

### Troubleshooting

If you encounter any issues with the application, please check the following:

- Ensure all dependencies are installed
- Verify that the database is properly initialized
- Check that both frontend and backend servers are running

For detailed troubleshooting information, see the [Troubleshooting Guide](docs/troubleshooting.md).

For database-specific issues, see the [Database Troubleshooting Guide](docs/database_troubleshooting.md).

## Manual Setup

If you prefer to set up the application manually:

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run database migrations:
   ```bash
   python migrate_db.py
   ```

6. Initialize the database:
   ```bash
   python init_db.py
   ```

7. Start the backend server:
   ```bash
   python run.py
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd mindfulwealth-react
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend server:
   ```bash
   npm start
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login a user
- `POST /api/auth/demo`: Create a demo user
- `POST /api/auth/refresh`: Refresh access token
- `GET /api/auth/me`: Get current user information

### Transactions

- `GET /api/transactions`: Get user transactions
- `POST /api/transactions`: Add a new transaction

### Budget

- `GET /api/budget`: Get user budget
- `POST /api/budget`: Update budget

### Saved Impulses

- `GET /api/saved-impulses`: Get saved impulses
- `POST /api/saved-impulses`: Add a new saved impulse

### Dashboard

- `GET /api/dashboard`: Get dashboard data

### Chat

- `POST /api/chat`: Send a message to the financial assistant

### Settings

- `GET /api/currency`: Get preferred currency
- `POST /api/currency`: Set preferred currency
- `POST /api/personality`: Set personality mode

## Authentication Flow

1. **Registration**: Users can register with a name, email, and password
2. **Login**: Users can login with their email and password
3. **Demo User**: Users can create a demo account without registration
4. **Token-based Authentication**: JWT tokens are used for authentication
   - Access token: Short-lived token for API access
   - Refresh token: Long-lived token for obtaining new access tokens

## Database Management

### Database Schema

The application uses SQLite for data storage with the following tables:
- `users`: Stores user information including authentication details
- `transactions`: Records financial transactions
- `budgets`: Stores budget information
- `saved_impulses`: Tracks saved impulse purchases

For a detailed description of the database schema, see [Database Schema Documentation](docs/database_schema.md).

### Database Migrations

The application includes a migration system to handle database schema changes:

1. **Automatic Migration**: The `migrate_db.py` script automatically updates the database schema when the application structure changes.
2. **Schema Recreation**: For significant changes, the migration script recreates tables while preserving existing data.
3. **Backup System**: Before any migration, the current database is backed up to `mindfulwealth.db.backup`.
4. **Field Name Compatibility**: The system handles discrepancies between frontend and backend field names.

For details on how we resolved a specific migration issue, see [Database Migration Summary](docs/database_migration_summary.md).

For a comprehensive overview of the database migration system improvements, see [Database Improvements](docs/database_improvements.md).

### Database Issues

If you encounter database-related errors (such as missing columns or tables), you can fix them by running:

```bash
chmod +x fix_database.sh
./fix_database.sh
```

This script will:
1. Back up your current database
2. Run the migration script to update the schema
3. Initialize the database with the updated schema

#### Common Database Errors

- **"no such column"**: Indicates the database schema is outdated
- **"Cannot add a UNIQUE column"**: Occurs when trying to add a column with a UNIQUE constraint to an existing table with data
- **"no such table"**: Indicates a missing table in the database

The migration system handles these errors by recreating tables with the new schema while preserving existing data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created as a demonstration of a full-stack financial wellness application.
- Icons provided by [Heroicons](https://heroicons.com/)
- UI components styled with [Tailwind CSS](https://tailwindcss.com/)

## Documentation

For detailed documentation about the application, please refer to the [Documentation Index](docs/README.md). 