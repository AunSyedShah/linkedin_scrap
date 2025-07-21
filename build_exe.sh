#!/bin/bash

# LinkedIn Scraper EXE Builder Script

echo "Building LinkedIn Scraper executable..."

# Activate virtual environment
source .venv/bin/activate

# Install PyInstaller if not already installed
pip install pyinstaller

# Create the executable
echo "Creating executable..."
pyinstaller --onefile --clean --name "LinkedInScraper" app.py

# Copy necessary files to dist folder
echo "Copying configuration files..."
cp credentials.txt dist/
cp search_phrases.txt dist/
cp README.md dist/

echo "Build completed!"
echo "Executable location: dist/LinkedInScraper"
echo "Don't forget to update credentials.txt and search_phrases.txt in the dist folder before running!"
