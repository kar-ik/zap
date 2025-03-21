#!/bin/bash

# Automated Setup Script for Vulnerability Scanner Tool

echo "Setting up the Vulnerability Scanner Tool..."

# Update package list and install dependencies
echo "Updating system packages..."
sudo apt update && sudo apt install -y python3 python3-pip npm

# Set up backend
echo "Setting up backend..."
pip install fastapi uvicorn requests

# Set up frontend
echo "Setting up frontend..."
npm install vite react react-dom axios

# Success message
echo "Setup complete! Run ./start.sh to launch the tool."
