@echo off
echo ====================================
echo  Success Diary - Install Dependencies
echo ====================================
echo.

:: Check if we're in the project root directory
if not exist "app\main.py" (
    echo ❌ ERROR: Please run this script from the project root directory
    echo    Current directory: %CD%
    echo    Expected to find: app\main.py and requirements.txt
    echo.
    echo    Correct usage:
    echo    cd C:\path\to\Success-Diary
    echo    scripts\windows\install-deps.bat
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ ERROR: requirements.txt not found in project root
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/updating dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Dependencies installed successfully!
) else (
    echo.
    echo ERROR: Failed to install dependencies
)

pause