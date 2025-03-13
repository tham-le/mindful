#!/bin/bash

# Run MindfulWealth application (frontend and backend)

# Start the backend
echo "Starting backend server..."
cd backend
python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Start the frontend
echo "Starting frontend server..."
cd mindfulwealth-react
npm start &
FRONTEND_PID=$!
cd ..

# Function to handle script termination
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Register the cleanup function for when script is terminated
trap cleanup SIGINT SIGTERM

echo "MindfulWealth is running!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop both servers."

# Keep the script running
wait 