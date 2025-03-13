#!/usr/bin/env python3
"""
Run script for MindfulWealth backend
"""
import os
import sys
import pathlib

# Try to import dotenv, but continue if not available
try:
    from dotenv import load_dotenv
    # Load environment variables
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables from system.")

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import models after adding current directory to path
from models import Base
from sqlalchemy import create_engine

# Ensure database is initialized
def init_db():
    """Initialize the database if it doesn't exist"""
    DB_PATH = pathlib.Path(__file__).parent / "mindfulwealth.db"
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    print(f"Database initialized at {DB_PATH}")

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Import app after initializing database
    from app import app
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5001))
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=port) 