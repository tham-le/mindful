#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   MindfulWealth Database Fix Script  ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Check if backend directory exists
if [ ! -d "backend" ]; then
  echo -e "${RED}Error: backend directory not found.${NC}"
  exit 1
fi

# Go to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo -e "${RED}Error: Virtual environment not found.${NC}"
  echo -e "${YELLOW}Please run ./setup.sh first to set up the environment.${NC}"
  exit 1
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating Python virtual environment...${NC}"
source venv/bin/activate

# Check if database exists
if [ ! -f "mindfulwealth.db" ]; then
  echo -e "${RED}Error: Database file not found.${NC}"
  echo -e "${YELLOW}Creating a new database...${NC}"
  python init_db.py
  echo -e "${GREEN}Database created successfully!${NC}"
  exit 0
fi

# Backup the current database
echo -e "\n${YELLOW}Backing up current database...${NC}"
cp mindfulwealth.db mindfulwealth.db.backup
echo -e "${GREEN}Database backed up to mindfulwealth.db.backup${NC}"

# Run the migration script
echo -e "\n${YELLOW}Running database migration...${NC}"
python migrate_db.py

# Initialize the database
echo -e "\n${YELLOW}Initializing database...${NC}"
python init_db.py

echo -e "\n${GREEN}Database fix completed successfully!${NC}"
echo -e "${GREEN}You can now run the application with:${NC}"
echo -e "${YELLOW}./start.sh${NC}" 