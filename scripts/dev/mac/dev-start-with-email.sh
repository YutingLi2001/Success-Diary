#!/bin/bash

# Success Diary - Full Development Start (with email testing)
# This script starts both the FastAPI server and Mailpit for local email testing

set -e

echo "🚀 Starting Success Diary development environment..."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down development environment..."
    if [ ! -z "$MAILPIT_PID" ]; then
        kill $MAILPIT_PID 2>/dev/null || true
        echo "   ✅ Mailpit stopped"
    fi
    if [ ! -z "$FASTAPI_PID" ]; then
        kill $FASTAPI_PID 2>/dev/null || true
        echo "   ✅ FastAPI server stopped"
    fi
    echo "👋 Development environment stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if Mailpit is installed
if ! command -v mailpit &> /dev/null; then
    echo "📧 Installing Mailpit for email testing..."
    brew install mailpit
fi

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f mailpit 2>/dev/null || true
pkill -f uvicorn 2>/dev/null || true
sleep 2

# Start Mailpit in background
echo "📧 Starting Mailpit (email testing server)..."
mailpit > /dev/null 2>&1 &
MAILPIT_PID=$!
sleep 2

# Check if Mailpit started successfully
if ! curl -s http://localhost:8025 > /dev/null; then
    echo "❌ Failed to start Mailpit"
    exit 1
fi

echo "   ✅ Mailpit running on http://localhost:8025"

# Activate virtual environment
echo "🐍 Activating Python virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -d "venv/lib/python3.11/site-packages/fastapi" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start FastAPI server
echo "🌐 Starting FastAPI server..."
echo ""
echo "📧 Email Testing: http://localhost:8025"
echo "🌐 App Server: http://localhost:8000"
echo ""
echo "💡 Press Ctrl+C to stop both servers"
echo ""

# Start FastAPI server (this will block)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 3

# Check if FastAPI started successfully
if ! curl -s http://localhost:8000 > /dev/null; then
    echo "❌ Failed to start FastAPI server"
    cleanup
    exit 1
fi

echo "   ✅ FastAPI server running on http://localhost:8000"
echo ""
echo "🎉 Development environment ready!"
echo "   📧 View emails: http://localhost:8025"
echo "   🌐 Use app: http://localhost:8000"
echo ""

# Wait for processes to finish or be interrupted
wait $FASTAPI_PID