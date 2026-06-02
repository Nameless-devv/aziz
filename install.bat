@echo off
REM Qishloq xo'jaligi roboti - Windows O'rnatish Skripti

echo ================================
echo 🌾 Aziz Robo - O'rnatish Skripti
echo ================================
echo.

REM 1. Python tekshiramiz
echo 📍 Python tekshirilmoqda...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python topilmadi!
    echo Iltimos, Python 3.8+ o'rnating: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python topildi: %PYTHON_VERSION%
echo.

REM 2. Virtual environment yaratamiz
echo 📍 Virtual environment o'rnatilmoqda...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment yaratildi
) else (
    echo ✅ Virtual environment allaqachon mavjud
)
echo.

REM 3. Virtual environment faollashtirish
echo 📍 Virtual environment faollashtirilyapti...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Virtual environment faol qila olmadi
    pause
    exit /b 1
)
echo ✅ Virtual environment faol
echo.

REM 4. Pip yangilaymiz
echo 📍 Pip yangilanmoqda...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo ✅ Pip yangilandi
echo.

REM 5. Zависимостиlarni o'rnatamiz
echo 📍 Zависимостиlar o'rnatilmoqda...
if exist "requirements.txt" (
    pip install -r requirements.txt
)
echo ✅ Zависимостilar o'rnatildi
echo.

REM 6. Proyektni o'rnatamiz
echo 📍 Proyekt o'rnatilmoqda...
pip install -e .
echo ✅ Proyekt o'rnatildi
echo.

REM 7. Batch skripti yaratamiz
echo 📍 Batch skripti yaratilmoqda...
setlocal enabledelayedexpansion
set "SCRIPT_PATH=%~dp0"
(
    echo @echo off
    echo chdir /d "%SCRIPT_PATH%"
    echo call venv\Scripts\activate.bat
    echo aziz %%*
) > "%SCRIPT_PATH%aziz.bat"
echo ✅ Batch skripti yaratildi
echo.

echo ================================
echo ✅ O'rnatish muvaffaqiyatli!
echo ================================
echo.
echo 📌 Foydalanish:
echo    Terminal qayta ochin yoki:
echo    venv\Scripts\activate
echo    aziz
echo.
echo 🚀 Boshlash uchun (CMD yoki PowerShell):
echo    aziz
echo.
pause
