#!/bin/bash
set -e

echo "===================================="
echo "   Success Diary - Reset Database"
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

# Check if database exists
if [ -f "db.sqlite3" ]; then
    echo "WARNING: This will delete all data in your database!"
    while true; do
        read -p "Are you sure you want to continue? (y/n): " confirm
        
        # Get first character and convert to lowercase
        first_char=$(echo "$confirm" | cut -c1 | tr '[:upper:]' '[:lower:]')
        
        if [ "$first_char" = "y" ]; then
            echo "Proceeding with database reset..."
            echo "Deleting database..."
            
            if rm db.sqlite3 2>/dev/null; then
                echo "Database deleted successfully!"
                break
            else
                echo "ERROR: Failed to delete database!"
                echo "The file may be in use by the server or another process."
                echo "Please stop the server first and try again."
                echo
                echo "Database reset failed - no changes were made."
                read -p "Press any key to continue..."
                exit 1
            fi
        elif [ "$first_char" = "n" ]; then
            echo "Operation cancelled."
            echo
            read -p "Press any key to continue..."
            exit 0
        else
            echo "Please type y or n"
        fi
    done
else
    echo "No database file found (db.sqlite3)"
fi

echo
echo "Database reset complete."
echo "The database will be recreated when you start the server next time."
read -p "Press any key to continue..."