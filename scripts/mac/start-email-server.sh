#!/bin/bash

# Start just the email testing server (Mailpit)
# Use this if you want to run email server separately

echo "📧 Starting Mailpit email testing server..."

# Check if Mailpit is installed
if ! command -v mailpit &> /dev/null; then
    echo "Installing Mailpit..."
    brew install mailpit
fi

# Kill existing mailpit processes
pkill -f mailpit 2>/dev/null || true
sleep 1

# Start Mailpit
echo "🚀 Starting Mailpit on http://localhost:8025"
mailpit

# When this exits, Mailpit stops