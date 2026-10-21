@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" call install.bat
.venv\Scripts\python.exe -m uvicorn app.web:app --host 0.0.0.0 --port 8000
