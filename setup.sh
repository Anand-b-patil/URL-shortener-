#!/bin/bash
# Setup script for Linux/Mac users

echo "========================================"
echo " Smart URL Shortener - Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

echo "✓ Python is installed"
python3 --version
echo ""

# Create directories
echo "Creating project directories..."
mkdir -p templates static/css static/js

# Move template files
if [ -f "index_template.html" ]; then
    mv index_template.html templates/index.html
    echo "✓ Moved index.html"
fi

if [ -f "dashboard_template.html" ]; then
    mv dashboard_template.html templates/dashboard.html
    echo "✓ Moved dashboard.html"
fi

if [ -f "404_template.html" ]; then
    mv 404_template.html templates/404.html
    echo "✓ Moved 404.html"
fi

if [ -f "expired_template.html" ]; then
    mv expired_template.html templates/expired.html
    echo "✓ Moved expired.html"
fi

if [ -f "500_template.html" ]; then
    mv 500_template.html templates/500.html
    echo "✓ Moved 500.html"
fi

echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo " ✓ Setup Complete!"
    echo "========================================"
    echo ""
    echo "To run the application:"
    echo "  python3 app.py"
    echo ""
    echo "Then open: http://localhost:5000"
    echo ""
else
    echo "❌ ERROR: Failed to install dependencies"
    exit 1
fi
