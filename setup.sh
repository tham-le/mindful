#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   MindfulWealth Setup Script         ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists python3; then
  echo -e "${RED}Error: python3 is not installed. Please install Python 3.${NC}"
  exit 1
fi

if ! command_exists pip3; then
  echo -e "${RED}Error: pip3 is not installed. Please install pip.${NC}"
  echo -e "${YELLOW}You can install it with: sudo apt install python3-pip${NC}"
  exit 1
fi

if ! command_exists npm; then
  echo -e "${RED}Error: npm is not installed. Please install Node.js and npm.${NC}"
  echo -e "${YELLOW}You can install it with: sudo apt install nodejs npm${NC}"
  exit 1
fi

# Check if backend directory exists
if [ ! -d "backend" ]; then
  echo -e "${RED}Error: backend directory not found.${NC}"
  exit 1
fi

# Check if frontend directory exists
if [ ! -d "mindfulwealth-react" ]; then
  echo -e "${RED}Error: mindfulwealth-react directory not found.${NC}"
  exit 1
fi

# Check for .env file and create if it doesn't exist
if [ ! -f "backend/.env" ]; then
  echo -e "${YELLOW}Warning: No .env file found in backend directory.${NC}"
  if [ -f "backend/.env.example" ]; then
    echo -e "${YELLOW}Creating a default .env file from .env.example. Please update with your API key.${NC}"
    cp backend/.env.example backend/.env
  else
    echo -e "${YELLOW}Creating a default .env file. Please update with your API key.${NC}"
    cat > backend/.env << EOF
# MindfulWealth API Configuration

# Database settings
DB_PATH=mindfulwealth.db

# API settings
PORT=5000
HOST=0.0.0.0

# JWT settings
JWT_SECRET_KEY=mindfulwealth-secret-key-change-in-production

# CORS settings
CORS_ORIGINS=http://localhost:3000
EOF
  fi
fi

# Create and set up Python virtual environment
cd backend
echo -e "\n${YELLOW}Setting up Python virtual environment...${NC}"

# Check if python3-venv is installed
if ! python3 -m venv --help > /dev/null 2>&1; then
  echo -e "${RED}Error: python3-venv is not installed.${NC}"
  echo -e "${YELLOW}You can install it with: sudo apt install python3-venv${NC}"
  exit 1
fi

# Remove existing venv if it exists but is broken
if [ -d "venv" ]; then
  echo -e "${YELLOW}Removing existing virtual environment...${NC}"
  rm -rf venv
fi

# Create a new virtual environment
echo -e "${YELLOW}Creating new Python virtual environment...${NC}"
python3 -m venv venv

# Check if venv was created successfully
if [ ! -d "venv" ]; then
  echo -e "${RED}Failed to create virtual environment.${NC}"
  exit 1
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating Python virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Make migration script executable
echo -e "\n${YELLOW}Setting up database migration...${NC}"
chmod +x migrate_db.py

# Run database migration
echo -e "\n${YELLOW}Running database migration...${NC}"
python migrate_db.py

# Initialize the database
echo -e "\n${YELLOW}Initializing database...${NC}"
python init_db.py

echo -e "\n${GREEN}Backend setup completed successfully!${NC}"

# Go to frontend directory
cd ../mindfulwealth-react

# Install frontend dependencies
echo -e "\n${YELLOW}Installing frontend dependencies...${NC}"
npm install

echo -e "\n${GREEN}Frontend setup completed successfully!${NC}"

cd ..

echo -e "\n${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}You can now run the application with:${NC}"
echo -e "${YELLOW}./start.sh${NC}" 