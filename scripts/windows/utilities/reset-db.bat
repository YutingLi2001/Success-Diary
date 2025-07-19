@echo off
setlocal enableextensions enabledelayedexpansion
echo ====================================
echo   Success Diary - Reset Database
echo ====================================
echo.

:: Change to project root directory (three levels up from scripts/windows/utilities)
cd /d "%~dp0..\..\\.."

:: Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: Could not find project root directory
    echo Expected to find app\main.py in: %CD%
    pause
    exit /b 1
)

:: Check if database exists
if exist "db.sqlite3" (
    set "db_file=db.sqlite3"
    goto prompt
) else (
    echo No database file found (db.sqlite3)
    goto end
)

:prompt
echo WARNING: This will delete all data in your database!
:ask
set /p confirm="Are you sure you want to continue? (y/n): "

:: Get first character and convert to lowercase for comparison
set "first_char=!confirm:~0,1!"
if /i "!first_char!"=="y" goto delete
if /i "!first_char!"=="n" goto cancel

echo Please type y or n
goto ask

:delete
echo Proceeding with database reset...
echo Deleting database: %db_file%
del "%db_file%" 2>nul
if exist "%db_file%" (
    echo ERROR: Failed to delete database!
    echo The file may be in use by the server or another process.
    echo Please stop the server first and try again.
    goto error_end
) else (
    echo Database deleted successfully!
    goto success_end
)

:cancel
echo Operation cancelled.
goto cancel_end

:end
echo.
echo No database changes were made.
pause
endlocal
exit /b 0

:success_end
echo.
echo Database reset complete.
echo The database will be recreated when you start the server next time.
pause
endlocal
exit /b 0

:cancel_end
echo.
pause
endlocal
exit /b 0

:error_end
echo.
echo Database reset failed - no changes were made.
pause
endlocal
exit /b 1