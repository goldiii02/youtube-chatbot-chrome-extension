#!/bin/bash

echo "Starting YouTube Chatbot Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Copy env.example to .env and add your API keys."
    echo ""
    read -p "Press enter to continue anyway..."
fi

# Start server
echo ""
echo "Starting FastAPI server..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
python main.py

