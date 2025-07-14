@echo off
echo 📧 Starting Mailpit email testing server...

:: Check if we're in the project root directory
if not exist "app\main.py" (
    echo ❌ ERROR: Please run this script from the project root directory
    echo    Current directory: %CD%
    echo    Expected to find: app\main.py
    echo.
    echo    Correct usage:
    echo    cd C:\path\to\Success-Diary
    echo    scripts\windows\start-email-server.bat
    pause
    exit /b 1
)

:: Check if Mailpit is installed
mailpit --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Mailpit not found. Please install it first:
    echo.
    echo Option 1 - Download binary:
    echo   Visit: https://github.com/axllent/mailpit/releases
    echo   Download the Windows version and add to PATH
    echo.
    echo Option 2 - Use Docker:
    echo   docker run -d -p 1025:1025 -p 8025:8025 axllent/mailpit
    echo.
    echo Option 3 - Use Chocolatey:
    echo   choco install mailpit
    echo.
    pause
    exit /b 1
)

:: Kill existing mailpit processes
echo 🧹 Stopping any existing Mailpit processes...
taskkill /f /im mailpit.exe >nul 2>&1 || echo    (No existing processes found)
timeout /t 1 >nul

:: Start Mailpit
echo 🚀 Starting Mailpit on http://localhost:8025
echo 💡 Press Ctrl+C to stop the email server
echo.

mailpit

echo.
echo 📧 Mailpit stopped.
pause