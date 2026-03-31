@echo off
echo ========================================
echo  Smart URL Shortener - File Organizer
echo ========================================
echo.
echo This script will organize your project files...
echo.

REM Create directories if they don't exist
if not exist "templates" mkdir templates
if not exist "static" mkdir static
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js

REM Move template files to templates directory
echo Moving template files...

if exist "index_template.html" (
    move /Y "index_template.html" "templates\index.html"
    echo ✓ Moved index.html to templates/
)

if exist "dashboard_template.html" (
    move /Y "dashboard_template.html" "templates\dashboard.html"
    echo ✓ Moved dashboard.html to templates/
)

if exist "404_template.html" (
    move /Y "404_template.html" "templates\404.html"
    echo ✓ Moved 404.html to templates/
)

if exist "expired_template.html" (
    move /Y "expired_template.html" "templates\expired.html"
    echo ✓ Moved expired.html to templates/
)

if exist "500_template.html" (
    move /Y "500_template.html" "templates\500.html"
    echo ✓ Moved 500.html to templates/
)

echo.
echo ========================================
echo  ✓ File organization complete!
echo ========================================
echo.
echo Project structure:
echo.
echo url-shortener/
echo ├── app.py
echo ├── requirements.txt
echo ├── templates/
echo │   ├── index.html
echo │   ├── dashboard.html
echo │   ├── 404.html
echo │   ├── expired.html
echo │   └── 500.html
echo └── static/
echo.
echo Next steps:
echo 1. Run: pip install -r requirements.txt
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
pause
