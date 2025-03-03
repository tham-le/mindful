#!/bin/bash

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists python3; then
  echo "Error: python3 is required but not installed."
  exit 1
fi

if ! command_exists npm; then
  echo "Error: npm is required but not installed."
  exit 1
fi

# Check if backend directory exists
if [ ! -d "backend" ]; then
  echo "Error: backend directory not found."
  exit 1
fi

# Check if frontend directory exists
if [ ! -d "mindfulwealth" ]; then
  echo "Error: mindfulwealth directory not found."
  exit 1
fi

# Check for .env file and create if it doesn't exist
if [ ! -f "backend/.env" ]; then
  echo "Warning: No .env file found in backend directory."
  echo "Creating a default .env file. Please update with your API key."
  cp backend/.env.example backend/.env
fi

# Start the backend server
echo "Starting Flask backend server..."
cd backend
python3 app.py &
BACKEND_PID=$!
BACKEND_EXIT_CODE=$?

if [ $BACKEND_EXIT_CODE -ne 0 ]; then
  echo "Error: Failed to start backend server."
  exit 1
fi

cd ..

# Start the frontend server
echo "Starting Vue.js frontend server..."
cd mindfulwealth
npm run dev &
FRONTEND_PID=$!
FRONTEND_EXIT_CODE=$?

if [ $FRONTEND_EXIT_CODE -ne 0 ]; then
  echo "Error: Failed to start frontend server."
  kill $BACKEND_PID
  exit 1
fi

cd ..

# Function to handle script termination
function cleanup {
  echo "Stopping servers..."
  kill $BACKEND_PID 2>/dev/null
  kill $FRONTEND_PID 2>/dev/null
  echo "Servers stopped."
  exit
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT SIGTERM

echo "Both servers are running!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:5000"
echo "Press Ctrl+C to stop both servers."

# Check if servers are still running every 5 seconds
while true; do
  if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Backend server stopped unexpectedly."
    kill $FRONTEND_PID 2>/dev/null
    exit 1
  fi
  
  if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "Frontend server stopped unexpectedly."
    kill $BACKEND_PID 2>/dev/null
    exit 1
  fi
  
  sleep 5
done 