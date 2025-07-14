#!/bin/bash
set -e

echo "===================================="
echo "   Success Diary - Quick Start"
echo "===================================="
echo

# Check if we're in the project root directory
if [ ! -f "app/main.py" ]; then
    echo "❌ ERROR: Please run this script from the project root directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected to find: app/main.py"
    echo ""
    echo "   Correct usage:"
    echo "   cd /path/to/Success-Diary"
    echo "   ./scripts/mac/quick-start.sh"
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