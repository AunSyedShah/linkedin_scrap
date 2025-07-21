#!/bin/bash

# LinkedIn Scraper Setup Script

echo "Setting up LinkedIn Scraper..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup completed!"
echo ""
echo "To run the scraper:"
echo "1. Edit credentials.txt with your LinkedIn credentials"
echo "2. Edit search_phrases.txt with your search terms"
echo "3. Run: python app.py"
