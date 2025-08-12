#!/bin/bash

# Azure App Service startup script
# This script is used by Azure App Service to start the application

echo "Starting Azure App Service application..."

# Set the port for Azure App Service
export PORT=8000

# Add src directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)/src"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Install dependencies if needed
if [ ! -f ".venv/bin/python" ]; then
    echo "Setting up virtual environment and installing dependencies..."
    uv venv
    source .venv/bin/activate
    uv sync
fi

# Start the Flask application
echo "Starting Flask application on port $PORT..."
python -m src.main
