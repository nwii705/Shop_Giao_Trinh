@echo off
echo ========================================
echo   EduShop - Seed du lieu mau
echo ========================================
echo.

cd /d "%~dp0"

echo Dang seed du lieu vao MongoDB...
curl -X POST http://localhost:5000/api/seed

echo.
echo ========================================
echo   Hoan tat! Refresh trang web de xem.
echo ========================================
pause
