@echo off
echo Creating project structure...

mkdir templates 2>nul
mkdir static 2>nul
mkdir static\css 2>nul
mkdir static\js 2>nul

echo ✓ Directories created successfully!
echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ✓ Setup complete!
echo.
echo To run the application:
echo   python app.py
pause
