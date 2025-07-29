#!/bin/bash

echo "Starting FastAPI MVC Development Server..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing/Updating requirements..."
pip install -r requirements.txt

# Initialize database if not exists
if [ ! -f "app.db" ]; then
    echo "Initializing database..."
    python init_db.py
fi

# Start the application
echo
echo "Starting FastAPI application..."
echo "API Documentation will be available at: http://localhost:8000/docs"
echo "Application will be available at: http://localhost:8000"
echo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
