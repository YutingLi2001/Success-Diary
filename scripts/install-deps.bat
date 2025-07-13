@echo off
echo ====================================
echo  Success Diary - Install Dependencies
echo ====================================
echo.

:: Change to project root directory (parent of scripts folder)
cd /d "%~dp0.."

:: Check if we're in the right directory
if not exist "requirements.txt" (
    echo ERROR: Could not find project root directory
    echo Expected to find requirements.txt in: %CD%
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