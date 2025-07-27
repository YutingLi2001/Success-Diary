#!/bin/bash
echo "Starting Mailpit email testing server..."

# Auto-navigate to project root directory
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

# Check if Mailpit is available (try multiple locations)
MAILPIT_CMD=""
if command -v mailpit &> /dev/null; then
    MAILPIT_CMD="mailpit"
elif [ -f "/usr/local/bin/mailpit" ]; then
    MAILPIT_CMD="/usr/local/bin/mailpit"
elif [ -f "./mailpit" ]; then
    MAILPIT_CMD="./mailpit"
fi

if [ -z "$MAILPIT_CMD" ]; then
    echo "❌ Mailpit not found. Please install it first:"
    echo
    echo "🍺 Option 1 - Use Homebrew (Recommended):"
    echo "   brew install mailpit"
    echo
    echo "📦 Option 2 - Download binary:"
    echo "   Visit: https://github.com/axllent/mailpit/releases"
    echo "   Download the macOS version and add to PATH"
    echo
    echo "🐳 Option 3 - Use Docker:"
    echo "   docker run -d -p 1025:1025 -p 8025:8025 axllent/mailpit"
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Kill existing mailpit processes
echo "Stopping any existing Mailpit processes..."
pkill -f mailpit 2>/dev/null || echo "    (No existing processes found)"
sleep 1

# Start Mailpit
echo "Starting Mailpit on http://localhost:8025"
echo "Press Ctrl+C to stop the email server"
echo

$MAILPIT_CMD

echo
echo "Mailpit stopped."
read -p "Press Enter to continue..."