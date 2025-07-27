#!/bin/bash
echo "======================================"
echo "    Success Diary - Dev Startup"
echo "======================================"
echo

# Make script executable and run from any location
cd "$(dirname "$0")/../.."

# Verify we're in the correct directory
if [ ! -f "app/main.py" ]; then
    echo "ERROR: Could not find project root directory"
    echo "    Script location: $(dirname "$0")"
    echo "    Current directory: $(pwd)"
    echo "    Expected to find: app/main.py"
    echo
    echo "    Please ensure the script is in the correct location relative to the project."
    read -p "Press Enter to continue..."
    exit 1
fi

echo "[1/5] Checking virtual environment..."
# Check if virtual environment exists, create if missing
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found. Creating it now..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: Failed to create virtual environment"
        echo "Please ensure Python 3 is installed and try again"
        read -p "Press Enter to continue..."
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo "[2/5] Installing/updating dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    read -p "Press Enter to continue..."
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
    echo "Please make sure your Mailpit credentials are configured"
    read -p "Press Enter to continue..."
fi

echo "[5/5] Starting development server..."
echo
echo "======================================"
echo "  Server will start on port 8000"
echo "  Access app at: http://localhost:8000"
echo "  Press Ctrl+C to stop the server"
echo "======================================"
echo

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# If we get here, the server was stopped
echo
echo "Server stopped."
read -p "Press Enter to continue..."