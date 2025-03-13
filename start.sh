#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   MindfulWealth Application Starter   ${NC}"
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

if ! command_exists npm; then
  echo -e "${RED}Error: npm is not installed. Please install Node.js and npm.${NC}"
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

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
  echo -e "${YELLOW}Virtual environment not found. Running setup script first...${NC}"
  ./setup.sh
  if [ $? -ne 0 ]; then
    echo -e "${RED}Setup failed. Please run ./setup.sh manually and check for errors.${NC}"
    exit 1
  fi
fi

# Go to backend directory
cd backend

# Activate virtual environment
echo -e "\n${YELLOW}Activating Python virtual environment...${NC}"
source venv/bin/activate

# Check if activation was successful
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to activate virtual environment. Please run ./setup.sh to recreate it.${NC}"
  exit 1
fi

# Start backend in background
echo -e "\n${GREEN}Starting backend server...${NC}"
python run.py &
BACKEND_PID=$!

# Wait a moment to make sure the backend starts
sleep 2

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
  echo -e "${RED}Backend server failed to start. Please check the error messages above.${NC}"
  exit 1
fi

# Go to frontend directory
cd ../mindfulwealth-react

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
  echo -e "${YELLOW}Frontend dependencies not found. Installing...${NC}"
  npm install
  if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install frontend dependencies. Please run 'npm install' in the mindfulwealth-react directory.${NC}"
    kill $BACKEND_PID
    exit 1
  fi
fi

# Start frontend
echo -e "\n${GREEN}Starting frontend server...${NC}"
npm start &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
  echo -e "\n${YELLOW}Shutting down servers...${NC}"
  kill $BACKEND_PID 2>/dev/null
  kill $FRONTEND_PID 2>/dev/null
  exit 0
}

# Register the cleanup function for script termination
trap cleanup SIGINT SIGTERM

echo -e "\n${GREEN}Both servers are running!${NC}"
echo -e "${GREEN}Backend: http://localhost:5000${NC}"
echo -e "${GREEN}Frontend: http://localhost:3000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Wait for user to press Ctrl+C
wait 