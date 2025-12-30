@echo off
setlocal
cd /d "%~dp0"

if not exist .venv\Scripts\activate.bat (
    echo Virtual environment not found at .venv\Scripts\activate.bat
    echo Create it first, then rerun this script.
    exit /b 1
)

call .venv\Scripts\activate.bat
python rat_move.py
