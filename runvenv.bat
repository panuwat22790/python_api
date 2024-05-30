@echo off
REM Save the current directory
set CURRENT_DIR=%~dp0

REM Change directory to the script's directory
cd /d "%CURRENT_DIR%"

REM Activate the virtual environment
call .\venv\Scripts\activate

REM Run the Python script
main.py

REM Deactivate the virtual environment
deactivate
