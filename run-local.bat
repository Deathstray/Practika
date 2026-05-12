@echo off
setlocal EnableExtensions
set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend"
set "FRONTEND=%ROOT%frontend"
set "VENV=%BACKEND%\.venv"
set "VENV_PY=%VENV%\Scripts\python.exe"
set "VENV_PIP=%VENV%\Scripts\pip.exe"

echo =========================================
echo  Система диспетчеризации транспорта
echo  Локальный запуск (SQLite, без Docker)
echo =========================================
echo.

:: Проверяем Python
py -3 --version >nul 2>&1
if not errorlevel 1 ( set "PY=py -3" ) else (
    python --version >nul 2>&1
    if not errorlevel 1 ( set "PY=python" ) else (
        echo [ОШИБКА] Python не найден. Установите с https://python.org
        pause & exit /b 1
    )
)

:: Проверяем Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Node.js не найден. Установите с https://nodejs.org
    pause & exit /b 1
)

:: Создаём venv
if exist "%VENV_PY%" (
    echo [1/4] Виртуальное окружение уже есть.
) else (
    if exist "%VENV%" rmdir /s /q "%VENV%"
    echo [1/4] Создаём виртуальное окружение...
    %PY% -m venv "%VENV%"
    if errorlevel 1 ( echo [ОШИБКА] Не удалось создать venv & pause & exit /b 1 )
)

:: Копируем .env
if not exist "%BACKEND%\.env"  copy /Y "%BACKEND%\.env.example"  "%BACKEND%\.env"  >nul
if not exist "%FRONTEND%\.env" copy /Y "%FRONTEND%\.env.example" "%FRONTEND%\.env" >nul

:: Обновляем pip через python -m pip (единственный надёжный способ на Windows)
echo [2/4] Обновляем pip и устанавливаем зависимости...
"%VENV_PY%" -m pip install --upgrade pip -q 2>nul
:: Не проверяем errorlevel после upgrade pip — иногда возвращает ошибку даже при успехе

:: Устанавливаем зависимости проекта
"%VENV_PY%" -m pip install -r "%BACKEND%\requirements.txt"
if errorlevel 1 (
    echo.
    echo [ОШИБКА] Не удалось установить зависимости!
    echo Попробуйте удалить папку backend\.venv и запустить снова.
    pause & exit /b 1
)
echo     Готово.

:: Запуск бэкенда
echo [3/4] Запускаем бэкенд на http://127.0.0.1:8001 ...
start "Transport Backend ^(8001^)" /D "%BACKEND%" "%VENV_PY%" main.py

echo     Ждём 5 секунд пока бэкенд поднимется...
timeout /t 5 /nobreak >nul

:: Запуск фронтенда
echo [4/4] Запускаем фронтенд на http://localhost:3000 ...
echo     (npm install при первом запуске занимает 2-3 мин)
start "Transport Frontend ^(3000^)" /D "%FRONTEND%" cmd /k "npm install && npm run dev"

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
pause
endlocal
