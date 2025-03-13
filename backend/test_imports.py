#!/usr/bin/env python3
"""
Test script to check if we can import the required modules
"""
import sys
import os

print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    import flask
    print(f"Flask version: {flask.__version__}")
except ImportError as e:
    print(f"Error importing flask: {e}")

try:
    import flask_cors
    print(f"Flask-CORS version: {flask_cors.__version__}")
except ImportError as e:
    print(f"Error importing flask_cors: {e}")

try:
    import sqlalchemy
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")
except ImportError as e:
    print(f"Error importing sqlalchemy: {e}")

try:
    import dotenv
    print(f"python-dotenv version: {dotenv.__version__}")
except ImportError as e:
    print(f"Error importing dotenv: {e}")

try:
    import flask_jwt_extended
    print(f"Flask-JWT-Extended version: {flask_jwt_extended.__version__}")
except ImportError as e:
    print(f"Error importing flask_jwt_extended: {e}")

try:
    import werkzeug
    print(f"Werkzeug version: {werkzeug.__version__}")
except ImportError as e:
    print(f"Error importing werkzeug: {e}")

try:
    import jwt
    print(f"PyJWT version: {jwt.__version__}")
except ImportError as e:
    print(f"Error importing jwt: {e}")

try:
    import google.generativeai
    print(f"Google Generative AI version: {google.generativeai.__version__}")
except ImportError as e:
    print(f"Error importing google.generativeai: {e}")

# Try to import our own modules
try:
    from models import Base, User
    print("Successfully imported models")
except ImportError as e:
    print(f"Error importing models: {e}")

try:
    from services.gemini_service import GeminiService, GENAI_AVAILABLE
    print(f"Successfully imported GeminiService, GENAI_AVAILABLE={GENAI_AVAILABLE}")
except ImportError as e:
    print(f"Error importing gemini_service: {e}") 