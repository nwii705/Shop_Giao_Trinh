@echo off
title EduShop Server
cd /d "%~dp0backend"
echo ========================================
echo   EduShop Server
echo ========================================
:loop
node server.js
echo.
echo Server stopped. Restarting in 3 seconds...
timeout /t 3 /nobreak
goto loop
