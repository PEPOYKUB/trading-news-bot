@echo off
@where py >nul 2>&1
if errorlevel 1 (
  echo Python Launcher not found. Install Python 3.11 or newer first.
  exit /b 1
)
py -3 -m venv .venv
if errorlevel 1 (
  echo Could not create virtual environment.
  exit /b 1
)
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if not exist .env copy /Y .env.example .env
.venv\Scripts\python.exe -m app.main init-db
echo Installation complete.
