#!/bin/bash

# Start Script for Vulnerability Scanner Tool

echo "Starting the Vulnerability Scanner Tool..."

# Start backend
echo "Launching backend..."
uvicorn backend:app --host 0.0.0.0 --port 8000 &

# Start frontend
echo "Launching frontend..."
npm run dev --prefix frontend &

# Success message
echo "Tool is running! Open http://localhost:3000 in your browser."

# Keep the script running
wait
