#!/bin/bash
set -e

echo "===================================="
echo "  Success Diary - Install Dependencies"
echo "===================================="
echo

# Check if we're in the project root directory
if [ ! -f "app/main.py" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ ERROR: Please run this script from the project root directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected to find: app/main.py and requirements.txt"
    echo ""
    echo "   Correct usage:"
    echo "   cd /path/to/Success-Diary"
    echo "   ./scripts/mac/install-deps.sh"
    read -p "Press any key to continue..."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "Dependencies installed successfully!"
else
    echo
    echo "ERROR: Failed to install dependencies"
fi

read -p "Press any key to continue..."