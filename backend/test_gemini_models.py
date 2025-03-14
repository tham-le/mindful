#!/usr/bin/env python3
"""
Test script for Gemini API models
"""
import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the actual Python executable being used
python_executable = sys.executable
logger.info(f"Script running with Python: {python_executable}")

# API key from .env file or hardcoded for testing
try:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBl177F81w3ggeG1oZwqlkdETGPflTlZwY")
    logger.info("Loaded API key from .env file")
except ImportError:
    API_KEY = "AIzaSyBl177F81w3ggeG1oZwqlkdETGPflTlZwY"
    logger.info("Using hardcoded API key")

def check_package_installed(package_name):
    """Check if a package is installed"""
    try:
        # Try to import the package
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    logger.info(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logger.info(f"Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package_name}: {e}")
        return False

def test_gemini_models():
    """Test available Gemini models"""
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python executable: {sys.executable}")
    
    # Check if google-generativeai is installed
    if not check_package_installed("google.generativeai"):
        logger.warning("google-generativeai package not installed")
        if install_package("google-generativeai"):
            logger.info("Successfully installed google-generativeai")
        else:
            logger.error("Failed to install google-generativeai")
            return
    
    try:
        import google.generativeai as genai
        logger.info(f"Successfully imported google.generativeai version {genai.__version__}")
        
        # Configure the API
        genai.configure(api_key=API_KEY)
        logger.info("Configured API with key")
        
        # List available models
        logger.info("Listing available models...")
        models = genai.list_models()
        
        # Print all models
        logger.info("All available models:")
        for model in models:
            logger.info(f"- {model.name}")
        
        # Filter for Gemini models
        gemini_models = [model.name for model in models if 'gemini' in model.name.lower()]
        
        if not gemini_models:
            logger.error("No Gemini models found!")
            return
        
        logger.info(f"Found {len(gemini_models)} Gemini models:")
        for model in gemini_models:
            logger.info(f"- {model}")
        
        # Try each Gemini model
        working_models = []
        
        for model_name in gemini_models:
            logger.info(f"Testing model: {model_name}")
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, please respond with a simple 'Hello, I am working correctly!'")
                logger.info(f"Response from {model_name}: {response.text}")
                logger.info(f"Test successful for {model_name}!")
                working_models.append(model_name)
            except Exception as e:
                logger.error(f"Error with model {model_name}: {str(e)}")
        
        if working_models:
            logger.info(f"Working models: {working_models}")
            logger.info(f"Recommendation: Use model '{working_models[0]}' in your application")
            
            # Update the GeminiService class to use the working model
            update_gemini_service(working_models[0])
        else:
            logger.error("All models failed. Please check your API key and permissions.")
        
    except ImportError:
        logger.error("Error: google-generativeai package not installed")
        logger.error("Install with: pip install google-generativeai")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

def update_gemini_service(model_name):
    """Update the GeminiService class to use the working model"""
    try:
        gemini_service_path = os.path.join(os.path.dirname(__file__), "services", "gemini_service.py")
        
        if not os.path.exists(gemini_service_path):
            logger.error(f"GeminiService file not found at {gemini_service_path}")
            return
        
        logger.info(f"Updating GeminiService to use model: {model_name}")
        
        # Read the file
        with open(gemini_service_path, 'r') as f:
            content = f.read()
        
        # Check if we need to update the model name
        if "gemini-pro" in content and model_name != "gemini-pro":
            # Create a backup
            with open(f"{gemini_service_path}.bak", 'w') as f:
                f.write(content)
            logger.info(f"Created backup at {gemini_service_path}.bak")
            
            # Update the model name
            updated_content = content.replace("'gemini-pro'", f"'{model_name}'")
            
            # Write the updated content
            with open(gemini_service_path, 'w') as f:
                f.write(updated_content)
            
            logger.info(f"Updated GeminiService to use model: {model_name}")
        else:
            logger.info("No update needed for GeminiService")
    
    except Exception as e:
        logger.error(f"Error updating GeminiService: {str(e)}")

if __name__ == "__main__":
    test_gemini_models() 