@echo off
echo ====================================
echo  Recreating Virtual Environment
echo ====================================
echo.

:: Auto-navigate to project root directory (three levels up from scripts/windows/utilities)
cd /d "%~dp0..\..\\.."

:: Check if we're in the correct directory
if not exist "app\main.py" (
    echo ERROR: Could not find project root directory
    pause
    exit /b 1
)

echo Removing existing virtual environment...
if exist "venv" (
    rmdir /s /q venv
    echo Virtual environment removed.
) else (
    echo No existing virtual environment found.
)

echo.
echo Creating new virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo Virtual environment recreated successfully!
echo You can now run your development scripts.
echo ====================================
pause