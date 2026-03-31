@echo off
REM Fix runtime.txt to force Python 3.11.9 on Render

echo ========================================
echo Render Python 3.14 Fix Script
echo ========================================
echo.

echo Step 1: Recreating runtime.txt with correct format...
echo python-3.11.9> runtime.txt
echo ✓ runtime.txt created
echo.

echo Step 2: Verifying content...
type runtime.txt
echo.

echo Step 3: Committing to Git...
git add runtime.txt
git commit -m "Force Python 3.11.9 for Render deployment (fix psycopg2 compatibility)"
if %errorlevel% neq 0 (
    echo ⚠️  No changes to commit or git error
) else (
    echo ✓ Committed to Git
)
echo.

echo Step 4: Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Push failed - check your Git configuration
    pause
    exit /b 1
) else (
    echo ✓ Pushed to GitHub
)
echo.

echo ========================================
echo ✅ runtime.txt fixed and pushed!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Go to Render Dashboard: https://dashboard.render.com/
echo 2. Click your web service
echo 3. Go to "Environment" tab
echo 4. Add environment variable:
echo    - Key: PYTHON_VERSION
echo    - Value: 3.11.9
echo 5. Click "Manual Deploy" → "Clear build cache & deploy"
echo.
pause
