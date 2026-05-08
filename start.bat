@echo off
chcp 65001 > nul
echo ============================================
echo  Запуск системы диспетчеризации транспорта
echo ============================================
echo.

REM Проверяем что зависимости установлены
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Зависимости не установлены!
    echo Сначала запусти install.bat
    pause
    exit /b 1
)

echo Запускаю Backend (FastAPI)...
start "Backend - FastAPI" cmd /k "chcp 65001 > nul && cd /d "%~dp0backend" && echo Запуск сервера на http://localhost:8000 && echo Документация API: http://localhost:8000/docs && echo. && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Жду запуска бэкенда...
timeout /t 4 /nobreak > nul

echo Запускаю Frontend (Nuxt)...
start "Frontend - Nuxt" cmd /k "chcp 65001 > nul && cd /d "%~dp0frontend" && echo Запуск фронтенда на http://localhost:3000 && echo. && npm run dev"

echo.
echo ============================================
echo  Приложение запускается!
echo.
echo  Фронтенд:    http://localhost:3000
echo  Бэкенд API:  http://localhost:8000
echo  Swagger UI:  http://localhost:8000/docs
echo.
echo  Логины: dispatcher / employee1 / driver1
echo  Пароль: admin123
echo ============================================
echo.
echo Открываю браузер через 8 секунд...
timeout /t 8 /nobreak > nul
start http://localhost:3000
