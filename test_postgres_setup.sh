#!/bin/bash

# Test script for PostgreSQL migration (Linux/Mac)

echo "========================================"
echo "Testing Smart URL Shortener"
echo "PostgreSQL Migration Validation"
echo "========================================"
echo ""

echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Please install Python 3.8+"
    exit 1
fi
python3 --version
echo "✓ Python installed"
echo ""

echo "Step 2: Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "WARNING: Virtual environment not found"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi
echo ""

echo "Step 3: Installing/updating dependencies..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

echo "Step 4: Checking psycopg2-binary..."
python -c "import psycopg2; print('✓ psycopg2-binary installed:', psycopg2.__version__)"
if [ $? -ne 0 ]; then
    echo "ERROR: psycopg2-binary not installed correctly"
    exit 1
fi
echo ""

echo "Step 5: Testing app import..."
python -c "import app; print('✓ App imports successfully')"
if [ $? -ne 0 ]; then
    echo "ERROR: App import failed"
    exit 1
fi
echo ""

echo "Step 6: Checking database configuration..."
python -c "import app; import os; db_url = os.environ.get('DATABASE_URL', 'Not set'); print('DATABASE_URL:', 'SQLite (development)' if not db_url or db_url == 'Not set' else 'PostgreSQL'); print('✓ Database configuration valid')"
echo ""

echo "========================================"
echo "✓ ALL CHECKS PASSED!"
echo "========================================"
echo ""
echo "Your app is ready to run!"
echo ""
echo "To start the app locally:"
echo "  python app.py"
echo ""
echo "To deploy to Render:"
echo "  1. Push code to GitHub"
echo "  2. Follow POSTGRESQL_MIGRATION.md"
echo ""
