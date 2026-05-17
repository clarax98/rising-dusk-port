@echo off
:: Rising Dusk - Port Preparation (Windows launcher)
:: Double-click this file to prepare the port files.
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Download it from https://www.python.org/downloads/
    echo Make sure to tick "Add Python to PATH" during installation.
    pause
    exit /b 1
)
python "%~dp0prepare_port.py"
