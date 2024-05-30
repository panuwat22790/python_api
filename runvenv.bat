@echo off
set CURRENT_DIR=%~dp0
cd /d "%CURRENT_DIR%"
call .\venv\Scripts\activate
main.py
deactivate