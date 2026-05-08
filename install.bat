@echo off
chcp 65001 > nul
echo ============================================
echo  Установка зависимостей
echo ============================================
echo.

echo Проверяю Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Скачай и установи Python 3.11+ с https://python.org
    echo При установке обязательно отметь "Add Python to PATH"
    pause
    exit /b 1
)
python --version

echo.
echo Проверяю Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Node.js не найден!
    echo Скачай и установи Node.js 20+ с https://nodejs.org
    pause
    exit /b 1
)
node --version

echo.
echo [1/2] Устанавливаю Python-пакеты (backend)...
cd /d "%~dp0backend"
pip install -r requirements.txt
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить Python-пакеты
    pause
    exit /b 1
)

echo.
echo [2/2] Устанавливаю Node.js-пакеты (frontend)...
cd /d "%~dp0frontend"
npm install
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить Node.js-пакеты
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Готово! Теперь запусти start.bat
echo ============================================
pause
