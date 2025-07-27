#!/bin/bash
echo "======================================"
echo "  Success Diary - Install Dependencies"
echo "======================================"
echo

# Auto-navigate to project root directory (three levels up from scripts/mac/utilities)
cd "$(dirname "$0")/../../.."

# Verify we're in the correct directory
if [ ! -f "app/main.py" ]; then
    echo "❌ ERROR: Could not find project root directory"
    echo "    Script location: $(dirname "$0")"
    echo "    Current directory: $(pwd)"
    echo "    Expected to find: app/main.py and requirements.txt"
    echo
    echo "    Please ensure the script is in the correct location relative to the project."
    read -p "Press Enter to continue..."
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ ERROR: requirements.txt not found in project root"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ ERROR: Virtual environment not found"
    echo
    echo "Please run the initial setup first:"
    echo "   Double-click: scripts/mac/initial-setup.command"
    echo "   Or run: ./scripts/mac/utilities/reset-venv.command"
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "✅ Dependencies installed successfully!"
else
    echo
    echo "❌ ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again."
fi

read -p "Press Enter to continue..."