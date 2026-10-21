@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo ยังไม่ได้ติดตั้งระบบ กำลังเปิดตัวติดตั้ง...
  call install.bat
  if errorlevel 1 (
    echo ติดตั้งไม่สำเร็จ กรุณาตรวจสอบ Python และอินเทอร์เน็ต
    pause
    exit /b 1
  )
)
start "Trading News Bot" cmd /k ""%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0app\dashboard.py""
timeout /t 3 /nobreak >nul
start "" http://localhost:8501
endlocal
