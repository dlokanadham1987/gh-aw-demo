@echo off
REM ---------------------------------------------------------------------------
REM  run.bat — one-click launcher for the Mini Notes API (Windows)
REM
REM  What it does:
REM   1. Ensures a Python venv exists in .venv\
REM   2. Activates the venv
REM   3. Installs requirements if FastAPI is not yet installed
REM   4. Starts the uvicorn server with --reload on http://127.0.0.1:8000
REM
REM  Usage: double-click run.bat  (or run from CMD / PowerShell)
REM ---------------------------------------------------------------------------

setlocal
cd /d "%~dp0"

REM --- Step 1: ensure venv exists ---
if not exist ".venv\Scripts\python.exe" (
    echo [run.bat] Creating virtual environment in .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo [run.bat] ERROR: failed to create venv. Is Python installed and on PATH?
        pause
        exit /b 1
    )
)

REM --- Step 2: activate venv ---
call ".venv\Scripts\activate.bat"

REM --- Step 3: install requirements if FastAPI is missing ---
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [run.bat] Installing dependencies from requirements.txt ...
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [run.bat] ERROR: pip install failed.
        pause
        exit /b 1
    )
)

REM --- Step 4: launch uvicorn ---
echo.
echo [run.bat] Starting Mini Notes API at http://127.0.0.1:8000
echo [run.bat] Swagger UI:                http://127.0.0.1:8000/docs
echo [run.bat] Press Ctrl+C to stop.
echo.
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

endlocal
