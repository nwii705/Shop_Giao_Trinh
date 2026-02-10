@echo off
chcp 65001 >nul
title GiaoTrinh AI
color 0A

cd /d "%~dp0"

:: Kiểm tra và khởi động backend
echo [*] Khoi dong Backend...
start /min cmd /c "cd backend && call venv\Scripts\activate && python run.py"

:: Đợi backend khởi động
echo [*] Doi backend khoi dong...
timeout /t 5 /nobreak >nul

:: Khởi động Electron App
echo [*] Khoi dong GiaoTrinh AI...
cd frontend
call npx electron .
