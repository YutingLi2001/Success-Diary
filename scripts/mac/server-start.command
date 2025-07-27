#!/bin/bash
echo "======================================"
echo "   Success Diary - Quick Start"
echo "======================================"
echo

# Auto-navigate to project root directory
cd "$(dirname "$0")/../.."

# Verify we're in the correct directory
if [ ! -f "app/main.py" ]; then
    echo "❌ ERROR: Could not find project root directory"
    echo "    Script location: $(dirname "$0")"
    echo "    Current directory: $(pwd)"
    echo "    Expected to find: app/main.py"
    echo
    echo "    Please ensure the script is in the correct location relative to the project."
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ ERROR: Virtual environment not found"
    echo
    echo "Please run the initial setup first:"
    echo "   Double-click: scripts/mac/initial-setup.command"
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting development server..."
echo
echo "======================================"
echo "  Server starting on port 8000"
echo "  Access app at: http://localhost:8000"
echo "  Press Ctrl+C to stop the server"
echo "======================================"
echo

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo
echo "Server stopped."
read -p "Press Enter to continue..."