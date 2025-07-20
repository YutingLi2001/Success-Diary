@echo off
echo ====================================
echo  Success Diary - Install Dependencies
echo ====================================
echo.

:: Auto-navigate to project root directory (three levels up from scripts/windows/utilities)
cd /d "%~dp0..\..\\.."

:: Verify we're in the correct directory
if not exist "app\main.py" (
    echo ❌ ERROR: Could not find project root directory
    echo    Script location: %~dp0
    echo    Current directory: %CD%
    echo    Expected to find: app\main.py and requirements.txt
    echo.
    echo    Please ensure the script is in the correct location relative to the project.
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