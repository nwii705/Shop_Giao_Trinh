@echo off
echo ========================================
echo   EduShop - Khoi dong he thong
echo ========================================
echo.

echo [1/2] Khoi dong Backend Server...
cd /d "%~dp0backend"
start "EduShop Backend" cmd /k "node server.js"

echo [2/2] Mo trinh duyet...
timeout /t 3 /nobreak > nul
start http://localhost:5000

echo.
echo ========================================
echo   He thong da san sang!
echo   Web: http://localhost:5000
echo ========================================
pause
