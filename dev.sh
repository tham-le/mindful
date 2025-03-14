#!/bin/bash

# MindfulWealth Development Script
# This script sets up the development environment for MindfulWealth

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "====================================================="
echo "          MindfulWealth Development Script           "
echo "====================================================="
echo -e "${NC}"

# Check if ports are available
echo -e "${YELLOW}Checking if required ports are available...${NC}"
PORT_5000=$(lsof -i:5000 -t)
PORT_3000=$(lsof -i:3000 -t)

if [ ! -z "$PORT_5000" ]; then
    echo -e "${RED}Port 5000 is already in use. Please free up this port before continuing.${NC}"
    echo -e "${YELLOW}Process using port 5000: $(ps -p $PORT_5000 -o comm=)${NC}"
    exit 1
fi

if [ ! -z "$PORT_3000" ]; then
    echo -e "${RED}Port 3000 is already in use. Please free up this port before continuing.${NC}"
    echo -e "${YELLOW}Process using port 3000: $(ps -p $PORT_3000 -o comm=)${NC}"
    exit 1
fi

# Check if backend .env file exists
echo -e "${YELLOW}Checking if backend/.env file exists...${NC}"
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Creating backend/.env file from template...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}backend/.env file created. Please edit it with your configuration.${NC}"
    echo -e "${YELLOW}Do you want to edit the backend/.env file now? (y/n)${NC}"
    read -r edit_backend_env
    if [[ "$edit_backend_env" =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} backend/.env
    fi
fi

# Check if frontend .env file exists
echo -e "${YELLOW}Checking if mindfulwealth-react/.env file exists...${NC}"
if [ ! -f "mindfulwealth-react/.env" ]; then
    echo -e "${YELLOW}Creating mindfulwealth-react/.env file from template...${NC}"
    cp mindfulwealth-react/.env.example mindfulwealth-react/.env
    echo -e "${GREEN}mindfulwealth-react/.env file created.${NC}"
    echo -e "${YELLOW}Do you want to edit the mindfulwealth-react/.env file now? (y/n)${NC}"
    read -r edit_frontend_env
    if [[ "$edit_frontend_env" =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} mindfulwealth-react/.env
    fi
fi

# Validate Gemini API key
echo -e "${YELLOW}Validating Gemini API key...${NC}"
GEMINI_API_KEY=$(grep -oP 'GEMINI_API_KEY=\K.*' backend/.env)
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" == "your-api-key-here" ]; then
    echo -e "${RED}Invalid or missing Gemini API key in backend/.env${NC}"
    echo -e "${YELLOW}Please enter a valid Gemini API key:${NC}"
    read -r api_key
    sed -i "s|GEMINI_API_KEY=.*|GEMINI_API_KEY=$api_key|g" backend/.env
    echo -e "${GREEN}Gemini API key updated.${NC}"
else
    echo -e "${GREEN}Gemini API key found.${NC}"
fi

# Ask which components to start
echo -e "${YELLOW}Which components do you want to start?${NC}"
echo -e "1) Backend only"
echo -e "2) Frontend only"
echo -e "3) Both backend and frontend"
read -r -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo -e "${GREEN}Starting backend...${NC}"
        cd backend
        python -m flask run --host=0.0.0.0 --port=5000
        ;;
    2)
        echo -e "${GREEN}Starting frontend...${NC}"
        cd mindfulwealth-react
        npm start
        ;;
    3)
        echo -e "${GREEN}Starting both backend and frontend...${NC}"
        echo -e "${YELLOW}Starting backend in the background...${NC}"
        cd backend
        python -m flask run --host=0.0.0.0 --port=5000 &
        BACKEND_PID=$!
        echo -e "${GREEN}Backend started with PID: $BACKEND_PID${NC}"
        
        echo -e "${YELLOW}Starting frontend...${NC}"
        cd ../mindfulwealth-react
        npm start
        
        # When frontend is stopped, also stop the backend
        echo -e "${YELLOW}Stopping backend (PID: $BACKEND_PID)...${NC}"
        kill $BACKEND_PID
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}Development environment stopped.${NC}" 