#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   MindfulWealth Gemini API Setup     ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}Error: backend/.env file not found.${NC}"
    echo -e "${YELLOW}Please run ./setup.sh first to create the environment file.${NC}"
    exit 1
fi

# Prompt for Gemini API key
echo -e "\n${YELLOW}To enable AI-powered financial advice, you need a Google Gemini API key.${NC}"
echo -e "${YELLOW}You can get one for free at: https://ai.google.dev/${NC}"
echo -e "${YELLOW}After creating your API key, enter it below:${NC}"
read -p "Gemini API Key: " gemini_api_key

# Validate input
if [ -z "$gemini_api_key" ]; then
    echo -e "${RED}No API key provided. Using mock responses instead.${NC}"
    echo -e "${YELLOW}You can set up the API key later by running this script again.${NC}"
    exit 0
fi

# Update .env file
sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$gemini_api_key/" backend/.env

# Install required Python package
echo -e "\n${YELLOW}Installing Google Generative AI Python package...${NC}"
cd backend
source venv/bin/activate
pip install google-generativeai
cd ..

echo -e "\n${GREEN}Gemini API setup completed successfully!${NC}"
echo -e "${GREEN}You can now run the application with:${NC}"
echo -e "${YELLOW}./start.sh${NC}"
echo -e "\n${GREEN}Your financial assistant will now provide AI-powered advice!${NC}" 