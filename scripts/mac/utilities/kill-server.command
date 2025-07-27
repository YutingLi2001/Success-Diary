#!/bin/bash
echo "========================================"
echo "     Success-Diary Server Killer"
echo "========================================"
echo

# ===========================================
# PHASE 1: STANDARD PROCESS TERMINATION
# ===========================================
echo "[PHASE 1] Standard process termination..."

echo "Checking for processes on port 8000..."
port_pids=$(lsof -ti :8000 2>/dev/null)
if [ -n "$port_pids" ]; then
    echo "Found server processes on port 8000: $port_pids"
    echo "Attempting standard termination..."
    for pid in $port_pids; do
        echo "Killing process PID: $pid"
        kill -TERM $pid 2>/dev/null
    done
    sleep 2
else
    echo "No processes found on port 8000"
fi

echo "Checking for uvicorn/FastAPI processes..."
uvicorn_pids=$(pgrep -f "uvicorn\|fastapi\|main:app" 2>/dev/null)
if [ -n "$uvicorn_pids" ]; then
    echo "Found uvicorn processes: $uvicorn_pids"
    for pid in $uvicorn_pids; do
        echo "Killing uvicorn process PID: $pid"
        kill -TERM $pid 2>/dev/null
    done
    sleep 2
else
    echo "No uvicorn processes found"
fi

# ===========================================
# PHASE 2: AGGRESSIVE TERMINATION
# ===========================================
echo
echo "[PHASE 2] Aggressive process termination..."

# Check again for stubborn processes
port_pids=$(lsof -ti :8000 2>/dev/null)
if [ -n "$port_pids" ]; then
    echo "Found stubborn processes: $port_pids"
    for pid in $port_pids; do
        echo "Force killing PID: $pid"
        kill -KILL $pid 2>/dev/null
        
        # Kill parent processes too
        parent_pid=$(ps -o ppid= -p $pid 2>/dev/null | tr -d ' ')
        if [ -n "$parent_pid" ] && [ "$parent_pid" != "1" ]; then
            echo "Killing parent PID: $parent_pid"
            kill -KILL $parent_pid 2>/dev/null
        fi
    done
    sleep 1
fi

# Nuclear option - kill all python processes (be careful with this!)
python_pids=$(pgrep -f "python.*uvicorn\|python.*fastapi\|python.*main:app" 2>/dev/null)
if [ -n "$python_pids" ]; then
    echo "Nuclear option - killing related Python processes: $python_pids"
    for pid in $python_pids; do
        kill -KILL $pid 2>/dev/null
    done
fi

# ===========================================
# PHASE 3: NETWORK CLEANUP (macOS specific)
# ===========================================
echo
echo "[PHASE 3] Network cleanup..."

# Flush network caches
echo "Flushing DNS cache..."
sudo dscacheutil -flushcache 2>/dev/null || echo "DNS flush requires sudo (skipped)"

# Reset network connections (less aggressive on macOS)
echo "Clearing network state..."
sudo pfctl -f /etc/pf.conf 2>/dev/null || echo "pfctl reset requires sudo (skipped)"

# ===========================================
# PHASE 4: VERIFICATION
# ===========================================
echo
echo "[PHASE 4] Verification..."

sleep 3
remaining_pids=$(lsof -ti :8000 2>/dev/null)
if [ -n "$remaining_pids" ]; then
    echo "❌ FAILED: Port 8000 is still in use"
    echo "Current connections:"
    lsof -i :8000 2>/dev/null || echo "No detailed info available"
    echo
    echo "Manual steps required:"
    echo "1. Open Activity Monitor and look for Python/uvicorn processes"
    echo "2. Force quit any remaining server processes"
    echo "3. Try: sudo lsof -ti :8000 | xargs sudo kill -9"
    echo "4. Last resort: Restart your Mac"
else
    echo "✅ SUCCESS: Port 8000 is now free!"
    echo "Server has been completely terminated."
fi

echo
echo "========================================"
echo "           Process Complete"
echo "========================================"
read -p "Press Enter to continue..."