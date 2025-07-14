@echo off
echo ====================================
echo   Success Diary - Quick Start
echo ====================================
echo.

:: Check if we're in the project root directory
if not exist "app\main.py" (
    echo ❌ ERROR: Please run this script from the project root directory
    echo    Current directory: %CD%
    echo    Expected to find: app\main.py
    echo.
    echo    Correct usage:
    echo    cd C:\path\to\Success-Diary
    echo    scripts\windows\quick-start.bat
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting development server...
echo.
echo ====================================
echo  Server starting on port 8000
echo  Access app at: http://localhost:8000
echo  Press Ctrl+C to stop the server
echo ====================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Server stopped.
pause