#!/usr/bin/env python3
"""
Simple script to test the Gemini API directly
"""
import os
import sys

# Print Python information
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

# API key from environment variable or hardcoded for testing
API_KEY = "AIzaSyDQpUzWGOW-YjTwJPNUQEMRO-WNebVrBGw"

def test_gemini():
    """Test the Gemini API with a simple request"""
    try:
        import google.generativeai as genai
        print("Successfully imported google.generativeai")
        print(f"google.generativeai version: {genai.__version__}")
        
        # Configure the API
        genai.configure(api_key=API_KEY)
        print("Configured API with key")
        
        # List available models
        print("Listing available models...")
        models = genai.list_models()
        
        # Print all models
        print("\nAll available models:")
        for model in models:
            print(f"- {model.name}")
        
        # Filter for Gemini models
        gemini_models = [model.name for model in models if 'gemini' in model.name.lower()]
        
        if not gemini_models:
            print("\nNo Gemini models found!")
            return
        
        print(f"\nFound {len(gemini_models)} Gemini models:")
        for model in gemini_models:
            print(f"- {model}")
        
        # Try each Gemini model
        for model_name in gemini_models:
            print(f"\nTesting model: {model_name}")
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, please respond with a simple 'Hello, I am working correctly!'")
                print(f"Response from {model_name}:")
                print(response.text)
                print("Test successful!")
                
                # If we got a successful response, we can stop testing
                print(f"\nRecommendation: Use model '{model_name}' in your application")
                return
            except Exception as e:
                print(f"Error with model {model_name}: {str(e)}")
        
        print("\nAll models failed. Please check your API key and permissions.")
        
    except ImportError:
        print("Error: google-generativeai package not installed")
        print("Install with: pip install google-generativeai")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_gemini() 