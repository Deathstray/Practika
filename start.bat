@echo off
chcp 65001 > nul
echo =========================================
echo  Система диспетчеризации транспорта
echo  Локальный запуск (SQLite, без Docker)
echo =========================================
echo.

REM Проверяем зависимости
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Зависимости не установлены!
    echo Сначала запусти install.bat
    pause
    exit /b 1
)

echo [1/4] Создаём виртуальное окружение...
cd /d "%~dp0backend"
if not exist venv (
    python -m venv venv >nul 2>&1
)

echo [2/4] Обновляем pip и устанавливаем зависимости...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo     Готово.

echo [3/4] Запускаем бэкенд на http://127.0.0.1:8000 ...
start "Backend - FastAPI :8000" cmd /k "chcp 65001 > nul && cd /d "%~dp0backend" && call venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo     Ждём 5 секунд пока бэкенд поднимется...
timeout /t 5 /nobreak > nul

echo [4/4] Запускаем фронтенд на http://localhost:3000 ...
echo     (npm install при первом запуске занимает 2-3 мин)
start "Frontend - Nuxt :3000" cmd /k "chcp 65001 > nul && cd /d "%~dp0frontend" && npm install && npm run dev"

echo.
echo =========================================
echo  Дождитесь в окне бэкенда:
echo    Application startup complete.
echo.
echo  Дождитесь в окне фронтенда:
echo    Local: http://localhost:3000/
echo.
echo  Затем открывайте: http://localhost:3000
echo.
echo  Демо-аккаунты (пароль: admin123):
echo    dispatcher  /  employee1  /  driver1
echo =========================================
timeout /t 20 /nobreak > nul
start http://localhost:3000
pause
