#!/bin/bash

# MindfulWealth Deployment Script
# This script handles the deployment of the MindfulWealth application

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "====================================================="
echo "          MindfulWealth Deployment Script            "
echo "====================================================="
echo -e "${NC}"

# Check if Docker is installed
echo -e "${YELLOW}Checking if Docker is installed...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
echo -e "${YELLOW}Checking if Docker Compose is installed...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Check if ports are available
echo -e "${YELLOW}Checking if required ports are available...${NC}"
PORT_5000=$(lsof -i:5000 -t)
PORT_80=$(lsof -i:80 -t)
PORT_3000=$(lsof -i:3000 -t)

if [ ! -z "$PORT_5000" ]; then
    echo -e "${RED}Port 5000 is already in use. Please free up this port before continuing.${NC}"
    echo -e "${YELLOW}Process using port 5000: $(ps -p $PORT_5000 -o comm=)${NC}"
    exit 1
fi

if [ ! -z "$PORT_80" ]; then
    echo -e "${RED}Port 80 is already in use. Please free up this port before continuing.${NC}"
    echo -e "${YELLOW}Process using port 80: $(ps -p $PORT_80 -o comm=)${NC}"
    exit 1
fi

if [ ! -z "$PORT_3000" ]; then
    echo -e "${YELLOW}Warning: Port 3000 is already in use. The application will still be accessible on port 80.${NC}"
    echo -e "${YELLOW}Process using port 3000: $(ps -p $PORT_3000 -o comm=)${NC}"
fi

# Check if .env file exists
echo -e "${YELLOW}Checking if .env file exists...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please edit it with your configuration.${NC}"
    echo -e "${YELLOW}Do you want to edit the .env file now? (y/n)${NC}"
    read -r edit_env
    if [[ "$edit_env" =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
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

# Check if frontend .env.production file exists
echo -e "${YELLOW}Checking if mindfulwealth-react/.env.production file exists...${NC}"
if [ ! -f "mindfulwealth-react/.env.production" ]; then
    echo -e "${YELLOW}Creating mindfulwealth-react/.env.production file from template...${NC}"
    cp mindfulwealth-react/.env.example mindfulwealth-react/.env.production
    # Update API URL in .env.production
    sed -i 's|REACT_APP_API_URL=.*|REACT_APP_API_URL=http://localhost:5000/api|g' mindfulwealth-react/.env.production
    echo -e "${GREEN}mindfulwealth-react/.env.production file created.${NC}"
    echo -e "${YELLOW}Do you want to edit the mindfulwealth-react/.env.production file now? (y/n)${NC}"
    read -r edit_frontend_env
    if [[ "$edit_frontend_env" =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} mindfulwealth-react/.env.production
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

# Build and start the containers
echo -e "${YELLOW}Building and starting the containers...${NC}"
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check if containers are running
echo -e "${YELLOW}Checking if containers are running...${NC}"
if [ "$(docker ps -q -f name=mindfulwealth-backend)" ] && [ "$(docker ps -q -f name=mindfulwealth-frontend)" ]; then
    echo -e "${GREEN}Containers are running successfully!${NC}"
else
    echo -e "${RED}Containers failed to start. Please check the logs.${NC}"
    docker-compose logs
    exit 1
fi

# Print success message
echo -e "${GREEN}"
echo "====================================================="
echo "          MindfulWealth Deployment Complete          "
echo "====================================================="
echo -e "${NC}"
echo -e "${GREEN}The application is now running at:${NC}"
echo -e "${BLUE}Frontend: http://localhost${NC}"
echo -e "${BLUE}Backend API: http://localhost:5000/api${NC}"
echo -e "${GREEN}You can also access the frontend at:${NC}"
echo -e "${BLUE}http://localhost:3000${NC} (if port 3000 is available)"
echo -e "${YELLOW}To view logs, run:${NC}"
echo -e "${BLUE}docker-compose logs -f${NC}"
echo -e "${YELLOW}To stop the application, run:${NC}"
echo -e "${BLUE}docker-compose down${NC}"
echo -e "${GREEN}Thank you for using MindfulWealth!${NC}" 