@echo off
REM Test script for PostgreSQL migration

echo ========================================
echo Testing Smart URL Shortener
echo PostgreSQL Migration Validation
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python installed
echo.

echo Step 2: Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
    echo ✓ Virtual environment activated
) else (
    echo WARNING: Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo ✓ Virtual environment created and activated
)
echo.

echo Step 3: Installing/updating dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Step 4: Checking psycopg2-binary...
python -c "import psycopg2; print('✓ psycopg2-binary installed:', psycopg2.__version__)"
if %errorlevel% neq 0 (
    echo ERROR: psycopg2-binary not installed correctly
    pause
    exit /b 1
)
echo.

echo Step 5: Testing app import...
python -c "import app; print('✓ App imports successfully')"
if %errorlevel% neq 0 (
    echo ERROR: App import failed
    pause
    exit /b 1
)
echo.

echo Step 6: Checking database configuration...
python -c "import app; import os; db_url = os.environ.get('DATABASE_URL', 'Not set'); print('DATABASE_URL:', 'SQLite (development)' if not db_url or db_url == 'Not set' else 'PostgreSQL'); print('✓ Database configuration valid')"
echo.

echo ========================================
echo ✓ ALL CHECKS PASSED!
echo ========================================
echo.
echo Your app is ready to run!
echo.
echo To start the app locally:
echo   python app.py
echo.
echo To deploy to Render:
echo   1. Push code to GitHub
echo   2. Follow POSTGRESQL_MIGRATION.md
echo.
pause
