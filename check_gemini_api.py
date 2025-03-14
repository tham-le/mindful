#!/usr/bin/env python3
"""
Script to check if the Gemini API key is properly configured.
This script will:
1. Check if the GEMINI_API_KEY environment variable is set
2. Attempt to initialize the Gemini API client
3. Make a simple test request to verify the API key works
"""

import os
import sys
import time
from dotenv import load_dotenv

# ANSI color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
ENDC = '\033[0m'

def print_header():
    """Print a formatted header for the script."""
    print(f"\n{BLUE}{'=' * 50}{ENDC}")
    print(f"{BLUE}   Gemini API Configuration Check{ENDC}")
    print(f"{BLUE}{'=' * 50}{ENDC}\n")

def check_env_variable():
    """Check if the GEMINI_API_KEY environment variable is set."""
    print(f"{YELLOW}Checking for GEMINI_API_KEY environment variable...{ENDC}")
    
    # Try to load from .env file first
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print(f"{RED}❌ GEMINI_API_KEY environment variable not found.{ENDC}")
        print(f"\nPlease set the GEMINI_API_KEY environment variable by:")
        print(f"1. Creating a .env file in the backend directory with:")
        print(f"   GEMINI_API_KEY=your_api_key_here")
        print(f"2. Or setting it directly in your environment:")
        print(f"   export GEMINI_API_KEY=your_api_key_here\n")
        return False
    
    # Mask the API key for security
    masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:]
    print(f"{GREEN}✓ GEMINI_API_KEY found: {masked_key}{ENDC}")
    return api_key

def check_gemini_package():
    """Check if the google-generativeai package is installed."""
    print(f"\n{YELLOW}Checking for google-generativeai package...{ENDC}")
    try:
        import google.generativeai as genai
        print(f"{GREEN}✓ google-generativeai package is installed.{ENDC}")
        return genai
    except ImportError:
        print(f"{RED}❌ google-generativeai package not found.{ENDC}")
        print(f"\nPlease install the package with:")
        print(f"pip install google-generativeai\n")
        return None

def test_gemini_api(api_key, genai):
    """Test the Gemini API with a simple request."""
    print(f"\n{YELLOW}Testing Gemini API connection...{ENDC}")
    
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Get available models
        print(f"{YELLOW}Fetching available models...{ENDC}")
        try:
            models = genai.list_models()
            all_models = [model.name for model in models]
            gemini_models = [model.name for model in models if 'gemini' in model.name.lower()]
            
            if not gemini_models:
                print(f"{RED}❌ No Gemini models found.{ENDC}")
                print(f"{YELLOW}Available models:{ENDC}")
                for model in all_models:
                    print(f"  - {model}")
                return False
            
            print(f"{GREEN}✓ Found {len(gemini_models)} Gemini models:{ENDC}")
            for model in gemini_models:
                print(f"  - {model}")
            
            # Make a simple test request
            print(f"\n{YELLOW}Making a test request with the first available Gemini model...{ENDC}")
            
            # Use the first available Gemini model
            model_name = gemini_models[0]
            print(f"{YELLOW}Using model: {model_name}{ENDC}")
            
            try:
                model = genai.GenerativeModel(model_name)
                
                # Simple test prompt
                response = model.generate_content("Hello, please respond with a simple 'Hello, I am working correctly!'")
                
                print(f"{GREEN}✓ Test request successful!{ENDC}")
                print(f"\nResponse from Gemini API:")
                print(f"{BLUE}{response.text}{ENDC}")
                
                return True
            except Exception as model_error:
                print(f"{RED}❌ Error with model {model_name}: {str(model_error)}{ENDC}")
                
                # Try with a different model
                if len(gemini_models) > 1:
                    alt_model_name = gemini_models[1]
                    print(f"\n{YELLOW}Trying with alternative model: {alt_model_name}...{ENDC}")
                    
                    try:
                        alt_model = genai.GenerativeModel(alt_model_name)
                        alt_response = alt_model.generate_content("Hello, please respond with a simple 'Hello, I am working correctly!'")
                        
                        print(f"{GREEN}✓ Test request with alternative model successful!{ENDC}")
                        print(f"\nResponse from Gemini API:")
                        print(f"{BLUE}{alt_response.text}{ENDC}")
                        
                        print(f"\n{YELLOW}Recommendation: Update your code to use the model '{alt_model_name}' instead of '{model_name}'.{ENDC}")
                        
                        return True
                    except Exception as alt_error:
                        print(f"{RED}❌ Error with alternative model {alt_model_name}: {str(alt_error)}{ENDC}")
                
                return False
        except Exception as models_error:
            print(f"{RED}❌ Error fetching models: {str(models_error)}{ENDC}")
            return False
        
    except Exception as e:
        print(f"{RED}❌ Error testing Gemini API: {str(e)}{ENDC}")
        
        # Check for common errors
        error_str = str(e).lower()
        if "api key" in error_str or "authentication" in error_str:
            print(f"\n{YELLOW}This appears to be an API key issue. Please check that your API key is valid and has the necessary permissions.{ENDC}")
        elif "model" in error_str and ("not found" in error_str or "not available" in error_str):
            print(f"\n{YELLOW}This appears to be a model availability issue. The model may not be available in your region or for your API key.{ENDC}")
        elif "quota" in error_str or "rate" in error_str or "limit" in error_str:
            print(f"\n{YELLOW}This appears to be a quota or rate limit issue. You may have exceeded your API usage limits.{ENDC}")
        
        return False

def main():
    """Main function to run the checks."""
    print_header()
    
    # Step 1: Check environment variable
    api_key = check_env_variable()
    if not api_key:
        return False
    
    # Step 2: Check for the Gemini package
    genai = check_gemini_package()
    if not genai:
        return False
    
    # Step 3: Test the API
    success = test_gemini_api(api_key, genai)
    
    # Print summary
    print(f"\n{BLUE}{'=' * 50}{ENDC}")
    print(f"{BLUE}   Summary{ENDC}")
    print(f"{BLUE}{'=' * 50}{ENDC}")
    
    if success:
        print(f"\n{GREEN}✓ Gemini API is properly configured and working!{ENDC}")
        print(f"\nYou can now use the AI-powered features of MindfulWealth.")
    else:
        print(f"\n{RED}❌ Gemini API configuration check failed.{ENDC}")
        print(f"\nPlease check the error messages above and fix the issues.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 