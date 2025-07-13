#!/bin/bash
set -e

echo "===================================="
echo "   Success Diary - Dev Startup"
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

echo "[1/5] Checking virtual environment..."
# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found at 'venv/bin/activate'"
    echo "Please create virtual environment first: python3 -m venv venv"
    read -p "Press any key to continue..."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo "[2/5] Installing/updating dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    read -p "Press any key to continue..."
    exit 1
fi

echo "[3/5] Resetting database..."
# Delete existing database if it exists
if [ -f "db.sqlite3" ]; then
    echo "Deleting existing database..."
    rm db.sqlite3
    echo "Database deleted successfully"
else
    echo "No existing database found"
fi

echo "[4/5] Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found"
    echo "Please make sure your Mailtrap credentials are configured"
    read -p "Press any key to continue..."
fi

echo "[5/5] Starting development server..."
echo
echo "===================================="
echo "  Server will start on port 8000"
echo "  Access app at: http://localhost:8000"
echo "  Press Ctrl+C to stop the server"
echo "===================================="
echo

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# If we get here, the server was stopped
echo
echo "Server stopped."
read -p "Press any key to continue..."