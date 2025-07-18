@echo off
echo ====================================
echo   Success Diary - Quick Start
echo ====================================
echo.

:: Auto-navigate to project root directory
cd /d "%~dp0..\.."

:: Verify we're in the correct directory
if not exist "app\main.py" (
    echo ❌ ERROR: Could not find project root directory
    echo    Script location: %~dp0
    echo    Current directory: %CD%
    echo    Expected to find: app\main.py
    echo.
    echo    Please ensure the script is in the correct location relative to the project.
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