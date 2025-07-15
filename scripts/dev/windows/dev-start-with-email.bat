@echo off
setlocal EnableDelayedExpansion

echo 🚀 Starting Success Diary development environment...

:: Check if we're in the project root directory
if not exist "app\main.py" (
    echo ❌ ERROR: Please run this script from the project root directory
    echo    Current directory: %CD%
    echo    Expected to find: app\main.py
    echo.
    echo    Correct usage:
    echo    cd C:\path\to\Success-Diary
    echo    scripts\windows\dev-start-with-email.bat
    pause
    exit /b 1
)

:: Function to handle cleanup on exit
set "cleanup_performed=false"

:: Check if Mailpit is installed (Windows version would be different)
echo 📧 Note: For Windows, you can download Mailpit from: https://github.com/axllent/mailpit/releases
echo    Or use Docker: docker run -d -p 1025:1025 -p 8025:8025 axllent/mailpit
echo.

:: Kill any existing processes
echo 🧹 Cleaning up existing processes...
taskkill /f /im mailpit.exe >nul 2>&1 || echo    (No mailpit processes found)
taskkill /f /im python.exe >nul 2>&1 || echo    (No python processes found)
timeout /t 2 >nul

:: Check if mailpit is available
mailpit --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Mailpit not found. Please install it first:
    echo    Option 1: Download from https://github.com/axllent/mailpit/releases
    echo    Option 2: Use Docker: docker run -d -p 1025:1025 -p 8025:8025 axllent/mailpit
    echo.
    echo    Continuing without email testing...
    set "SKIP_MAILPIT=true"
) else (
    :: Start Mailpit in background
    echo 📧 Starting Mailpit (email testing server)...
    start /B mailpit
    timeout /t 3 >nul
    echo    ✅ Mailpit should be running on http://localhost:8025
)

:: Activate virtual environment
echo 🐍 Activating Python virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Please run: python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

:: Install dependencies if needed
if not exist "venv\Lib\site-packages\fastapi" (
    echo 📦 Installing Python dependencies...
    pip install -r requirements.txt
)

:: Display information
echo.
echo 📧 Email Testing: http://localhost:8025
echo 🌐 App Server: http://localhost:8000
echo.
echo 💡 Press Ctrl+C to stop both servers
echo.

:: Start FastAPI server
echo 🌐 Starting FastAPI server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo.
echo 🛑 Servers stopped.
echo 🧹 Cleaning up processes...
taskkill /f /im mailpit.exe >nul 2>&1 || echo    (No mailpit processes to clean)

pause