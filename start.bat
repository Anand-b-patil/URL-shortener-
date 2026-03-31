@echo off
echo ========================================
echo  Smart URL Shortener - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version
echo.

REM Check if templates directory exists
if not exist "templates\index.html" (
    echo ⚠ Templates directory is not set up yet.
    echo.
    echo Running file organizer...
    call organize.bat
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install dependencies
    echo.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✓ Setup Complete!
echo ========================================
echo.
echo Starting the application...
echo.
echo The app will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Start the application
python app.py

pause
