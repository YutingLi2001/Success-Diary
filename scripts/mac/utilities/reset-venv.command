#!/bin/bash
echo "======================================"
echo "  Recreating Virtual Environment"
echo "======================================"
echo

# Auto-navigate to project root directory (three levels up from scripts/mac/utilities)
cd "$(dirname "$0")/../../.."

# Check if we're in the correct directory
if [ ! -f "app/main.py" ]; then
    echo "ERROR: Could not find project root directory"
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Removing existing virtual environment..."
if [ -d "venv" ]; then
    rm -rf venv
    echo "Virtual environment removed."
else
    echo "No existing virtual environment found."
fi

echo
echo "Creating new virtual environment..."
python3 -m venv venv

echo
echo "Activating virtual environment..."
source venv/bin/activate

echo
echo "Upgrading pip..."
pip install --upgrade pip

echo
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "======================================"
    echo "Virtual environment recreated successfully!"
    echo "You can now run your development scripts."
    echo "======================================"
else
    echo
    echo "======================================"
    echo "ERROR: Failed to install dependencies!"
    echo "Please check requirements.txt and try again."
    echo "======================================"
fi

read -p "Press Enter to continue..."