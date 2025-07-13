@echo off
echo ====================================
echo   Success Diary - Quick Start
echo ====================================
echo.

:: Change to project root directory (two levels up from scripts/windows)
cd /d "%~dp0..\.."

:: Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: Could not find project root directory
    echo Expected to find app\main.py in: %CD%
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