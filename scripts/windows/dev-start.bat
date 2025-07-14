@echo off
echo ====================================
echo    Success Diary - Dev Startup
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
    echo    scripts\windows\dev-start.bat
    pause
    exit /b 1
)

echo [1/5] Checking virtual environment...
:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found at 'venv\Scripts\activate.bat'
    echo Please create virtual environment first: python -m venv venv
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/5] Installing/updating dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [3/5] Resetting database...
:: Delete existing database if it exists
if exist "db.sqlite3" (
    echo Deleting existing database...
    del db.sqlite3
    echo Database deleted successfully
) else (
    echo No existing database found
)

echo [4/5] Checking environment configuration...
if not exist ".env" (
    echo WARNING: .env file not found
    echo Please make sure your Mailtrap credentials are configured
    pause
)

echo [5/5] Starting development server...
echo.
echo ====================================
echo  Server will start on port 8000
echo  Access app at: http://localhost:8000
echo  Press Ctrl+C to stop the server
echo ====================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

:: If we get here, the server was stopped
echo.
echo Server stopped.
pause