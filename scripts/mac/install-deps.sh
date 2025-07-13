#!/bin/bash
set -e

echo "===================================="
echo "  Success Diary - Install Dependencies"
echo "===================================="
echo

# Change to project root directory (parent of scripts folder)
cd "$(dirname "$0")/../.."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found"
    echo "Please run this script from the success-diary project root directory"
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