#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   MindfulWealth Test Runner          ${NC}"
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

# Create tests directory if it doesn't exist
if [ ! -d "backend/tests" ]; then
  echo -e "${YELLOW}Creating tests directory in backend...${NC}"
  mkdir -p backend/tests
  touch backend/tests/__init__.py
fi

if [ ! -d "mindfulwealth-react/src/tests" ]; then
  echo -e "${YELLOW}Creating tests directory in frontend...${NC}"
  mkdir -p mindfulwealth-react/src/tests
fi

# Run backend tests
echo -e "\n${YELLOW}Running backend tests...${NC}"
cd backend
source venv/bin/activate

# Check if pytest is installed
if ! python -c "import pytest" &> /dev/null; then
  echo -e "${YELLOW}Installing pytest...${NC}"
  pip install pytest
fi

# Run the tests
python -m pytest tests/ -v

# Store the exit code
BACKEND_EXIT_CODE=$?

# Deactivate the virtual environment
deactivate

# Run frontend tests
echo -e "\n${YELLOW}Running frontend tests...${NC}"
cd ../mindfulwealth-react

# Check if testing libraries are installed
if [ ! -d "node_modules/@testing-library" ]; then
  echo -e "${YELLOW}Installing testing libraries...${NC}"
  npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
fi

# Run the tests
npm test -- --watchAll=false

# Store the exit code
FRONTEND_EXIT_CODE=$?

# Return to the root directory
cd ..

# Print summary
echo -e "\n${BLUE}=======================================${NC}"
echo -e "${BLUE}   Test Summary                        ${NC}"
echo -e "${BLUE}=======================================${NC}"

if [ $BACKEND_EXIT_CODE -eq 0 ]; then
  echo -e "${GREEN}Backend tests: PASSED${NC}"
else
  echo -e "${RED}Backend tests: FAILED${NC}"
fi

if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
  echo -e "${GREEN}Frontend tests: PASSED${NC}"
else
  echo -e "${RED}Frontend tests: FAILED${NC}"
fi

# Exit with an error if any tests failed
if [ $BACKEND_EXIT_CODE -ne 0 ] || [ $FRONTEND_EXIT_CODE -ne 0 ]; then
  echo -e "\n${RED}Some tests failed. Please check the output above for details.${NC}"
  exit 1
else
  echo -e "\n${GREEN}All tests passed!${NC}"
  exit 0
fi 