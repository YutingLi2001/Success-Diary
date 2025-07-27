#!/bin/bash
echo "================================================="
echo "  Success Diary - Initial Project Setup"
echo "================================================="
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

echo "✅ Found project directory: $(pwd)"
echo

echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 first:"
    echo "  Option 1: Download from https://www.python.org/downloads/"
    echo "  Option 2: Install via Homebrew: brew install python"
    read -p "Press Enter to continue..."
    exit 1
fi

python_version=$(python3 --version)
echo "✅ Found: $python_version"
echo

echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
    else
        echo "Skipping virtual environment creation"
        echo
        goto_deps=true
    fi
fi

if [ ! -d "venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: Failed to create virtual environment"
        read -p "Press Enter to continue..."
        exit 1
    fi
    echo "✅ Virtual environment created"
fi
echo

echo "[3/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to activate virtual environment"
    read -p "Press Enter to continue..."
    exit 1
fi
echo "✅ Virtual environment activated"
echo

echo "[4/5] Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ Pip upgraded"
echo

echo "[5/5] Installing project dependencies..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ ERROR: requirements.txt not found"
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo
    echo "================================================="
    echo "  🎉 Setup Complete!"
    echo "================================================="
    echo
    echo "Your development environment is ready to use:"
    echo
    echo "📱 Start development server:"
    echo "   ./scripts/mac/quick-start.sh"
    echo
    echo "📧 Start with email server:"
    echo "   ./scripts/mac/dev-start-with-email.sh"
    echo
    echo "🔧 Full development setup:"
    echo "   ./scripts/mac/dev-setup.command"
    echo
    echo "📋 Other utilities available in:"
    echo "   ./scripts/mac/utilities/"
    echo
else
    echo "❌ ERROR: Failed to install dependencies"
    echo
    echo "Please check:"
    echo "1. Internet connection"
    echo "2. Python version compatibility"
    echo "3. requirements.txt file"
    echo
fi

read -p "Press Enter to continue..."