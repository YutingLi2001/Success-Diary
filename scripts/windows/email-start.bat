@echo off
echo Starting Mailpit email testing server...

:: Auto-navigate to project root directory
cd /d "%~dp0..\.."

:: Verify we're in the correct directory
if not exist "app\main.py" (
    echo ERROR: Could not find project root directory
    echo    Script location: %~dp0
    echo    Current directory: %CD%
    echo    Expected to find: app\main.py
    echo.
    echo    Please ensure the script is in the correct location relative to the project.
    pause
    exit /b 1
)

:: Check if Mailpit is available (try multiple locations)
set "MAILPIT_CMD="
mailpit --version >nul 2>&1 && set "MAILPIT_CMD=mailpit"
if exist "C:\tools\mailpit.exe" set "MAILPIT_CMD=C:\tools\mailpit.exe"
if exist "mailpit.exe" set "MAILPIT_CMD=mailpit.exe"

if "%MAILPIT_CMD%"=="" (
    echo Mailpit not found. Please install it first:
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
echo Stopping any existing Mailpit processes...
taskkill /f /im mailpit.exe >nul 2>&1 || echo    (No existing processes found)
timeout /t 1 >nul

:: Start Mailpit
echo Starting Mailpit on http://localhost:8025
echo Press Ctrl+C to stop the email server
echo.

"%MAILPIT_CMD%"

echo.
echo Mailpit stopped.
pause