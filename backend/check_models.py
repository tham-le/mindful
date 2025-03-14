#!/usr/bin/env python3
"""
Script to check available Gemini models
"""
import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Set API key directly
api_key = "AIzaSyBl177F81w3ggeG1oZwqlkdETGPflTlZwY"

try:
    import google.generativeai as genai
    
    # Configure the API
    genai.configure(api_key=api_key)
    
    # List available models
    print("Available models:")
    models = genai.list_models()
    for model in models:
        print(f"- {model.name}")
        print(f"  Supported generation methods: {model.supported_generation_methods}")
    
    # Try to create a model
    print("\nTrying to create a model...")
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        print(f"Successfully created model: gemini-1.5-pro")
    except Exception as e:
        print(f"Error creating gemini-1.5-pro model: {e}")
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        print(f"Successfully created model: gemini-pro")
    except Exception as e:
        print(f"Error creating gemini-pro model: {e}")
    
    try:
        model = genai.GenerativeModel('gemini-1.0-pro')
        print(f"Successfully created model: gemini-1.0-pro")
    except Exception as e:
        print(f"Error creating gemini-1.0-pro model: {e}")
    
except ImportError:
    print("Failed to import google.generativeai. Make sure it's installed.")
except Exception as e:
    print(f"Error: {e}") 