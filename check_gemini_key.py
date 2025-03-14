#!/usr/bin/env python3
"""
Script to check if the Gemini API key is valid.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("Please set it in your .env file or environment.")
    sys.exit(1)

try:
    import google.generativeai as genai
    print("Successfully imported google.generativeai")
except ImportError:
    print("Error: google-generativeai package not installed.")
    print("Please install it with: pip install google-generativeai")
    sys.exit(1)

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Try to list available models
try:
    print("Checking available models...")
    models = genai.list_models()
    model_names = [model.name for model in models]
    print(f"Available models: {model_names}")
    
    # Find a suitable model
    gemini_models = [name for name in model_names if "gemini" in name.lower()]
    if not gemini_models:
        print("Warning: No Gemini models found. Your API key might not have access to Gemini models.")
        sys.exit(1)
    
    # Try to use the first available Gemini model
    model_name = gemini_models[0]
    print(f"Testing model: {model_name}")
    
    model = genai.GenerativeModel(model_name)
    
    # Try a simple generation
    response = model.generate_content("Hello, world!")
    print("Test response:", response.text)
    
    print("\nSuccess! Your Gemini API key is valid and working correctly.")
    
except Exception as e:
    print(f"Error: {str(e)}")
    print("\nYour Gemini API key might be invalid or expired.")
    print("Please get a new API key from https://ai.google.dev/ and update your .env file.")
    sys.exit(1) 