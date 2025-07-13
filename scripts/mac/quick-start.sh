#!/bin/bash
set -e

echo "===================================="
echo "   Success Diary - Quick Start"
echo "===================================="
echo

# Change to project root directory (parent of scripts folder)
cd "$(dirname "$0")/../.."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "ERROR: Could not find project root directory"
    echo "Expected to find app/main.py in: $(pwd)"
    read -p "Press any key to continue..."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting development server..."
echo
echo "===================================="
echo "  Server starting on port 8000"
echo "  Access app at: http://localhost:8000"
echo "  Press Ctrl+C to stop the server"
echo "===================================="
echo

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo
echo "Server stopped."
read -p "Press any key to continue..."