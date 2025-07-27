#!/bin/bash
echo "======================================"
echo "   Success Diary - Reset Database"
echo "======================================"
echo

# Change to project root directory (three levels up from scripts/mac/utilities)
cd "$(dirname "$0")/../../.."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "ERROR: Could not find project root directory"
    echo "Expected to find app/main.py in: $(pwd)"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if database exists
if [ -f "db.sqlite3" ]; then
    db_file="db.sqlite3"
else
    echo "No database file found (db.sqlite3)"
    echo
    echo "No database changes were made."
    read -p "Press Enter to continue..."
    exit 0
fi

echo "WARNING: This will delete all data in your database!"

while true; do
    read -p "Are you sure you want to continue? (y/n): " confirm
    case $confirm in
        [Yy]* ) 
            echo "Proceeding with database reset..."
            echo "Deleting database: $db_file"
            if rm "$db_file" 2>/dev/null; then
                echo "Database deleted successfully!"
                echo
                echo "Database reset complete."
                echo "The database will be recreated when you start the server next time."
            else
                echo "ERROR: Failed to delete database!"
                echo "The file may be in use by the server or another process."
                echo "Please stop the server first and try again."
                echo
                echo "Database reset failed - no changes were made."
                read -p "Press Enter to continue..."
                exit 1
            fi
            break
            ;;
        [Nn]* ) 
            echo "Operation cancelled."
            echo
            break
            ;;
        * ) 
            echo "Please type y or n"
            ;;
    esac
done

read -p "Press Enter to continue..."