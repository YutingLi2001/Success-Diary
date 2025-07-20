@echo off
setlocal enabledelayedexpansion
echo ========================================
echo     Success-Diary Server Killer
echo ========================================

REM Check admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

echo Running with administrator privileges...
echo.

REM ===========================================
REM PHASE 1: STANDARD PROCESS TERMINATION
REM ===========================================
echo [PHASE 1] Standard process termination...

echo Checking for processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Found server process PID: %%a
    echo Attempting standard termination...
    taskkill /PID %%a /F /T 2>nul
    timeout /t 2 /nobreak >nul
)

echo Checking for uvicorn/FastAPI processes...
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2^>nul ^| findstr python.exe') do (
    set pid=%%i
    set pid=!pid:"=!
    if not "!pid!"=="" (
        wmic process where "ProcessId=!pid!" get CommandLine 2>nul | findstr -i "uvicorn\|fastapi\|main:app" >nul
        if !errorlevel! equ 0 (
            echo Killing uvicorn process PID: !pid!
            taskkill /PID !pid! /F /T 2>nul
        )
    )
)

REM ===========================================
REM PHASE 2: AGGRESSIVE TERMINATION
REM ===========================================
echo.
echo [PHASE 2] Aggressive process termination...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Found stubborn PID: %%a
    
    echo Trying wmic termination...
    wmic process where "ProcessId=%%a" delete 2>nul
    
    echo Trying PowerShell termination...
    powershell -Command "Stop-Process -Id %%a -Force" 2>nul
    
    echo Checking for parent processes...
    for /f "tokens=2 delims==" %%b in ('wmic process where "ProcessId=%%a" get ParentProcessId /format:value 2^>nul ^| findstr ParentProcessId') do (
        if not "%%b"=="" (
            echo Killing parent PID: %%b
            taskkill /PID %%b /F /T 2>nul
        )
    )
    
    timeout /t 1 /nobreak >nul
)

REM Kill all python processes as nuclear option
echo Nuclear option - killing all Python processes...
taskkill /IM python.exe /F /T 2>nul

REM ===========================================
REM PHASE 3: ZOMBIE CONNECTION CLEANUP
REM ===========================================
echo.
echo [PHASE 3] Cleaning up zombie connections...

echo Checking for zombie connections...
netstat -ano | findstr :8000 | findstr LISTENING >nul
if !errorlevel! equ 0 (
    echo Found zombie connection. Resetting network stack...
    
    echo Flushing DNS...
    ipconfig /flushdns >nul
    
    echo Resetting Winsock...
    netsh winsock reset catalog >nul
    
    echo Resetting TCP/IP...
    netsh int ip reset reset.log >nul
    
    echo Resetting TCP connections...
    netsh int tcp reset >nul
    
    echo Stopping network services...
    net stop winnat 2>nul
    net stop "Windows NAT Driver" 2>nul
    timeout /t 2 /nobreak >nul
    
    echo Starting network services...
    net start winnat 2>nul
    net start "Windows NAT Driver" 2>nul
    timeout /t 2 /nobreak >nul
)

REM ===========================================
REM PHASE 4: VERIFICATION
REM ===========================================
echo.
echo [PHASE 4] Verification...

timeout /t 3 /nobreak >nul
netstat -ano | findstr :8000 | findstr LISTENING >nul
if !errorlevel! equ 0 (
    echo ❌ FAILED: Port 8000 is still in use
    echo Current connections:
    netstat -ano | findstr :8000
    echo.
    echo Manual steps required:
    echo 1. Open Task Manager as Admin ^> Services tab
    echo 2. Look for Python/web services and stop them
    echo 3. Restart "Windows NAT Driver" service in services.msc
    echo 4. Last resort: Restart network adapter in Device Manager
    echo 5. Reboot computer if all else fails
) else (
    echo ✅ SUCCESS: Port 8000 is now free!
    echo Server has been completely terminated.
)

echo.
echo ========================================
echo           Process Complete
echo ========================================
pause