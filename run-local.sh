#!/bin/bash
# Локальный запуск без Docker (Linux/macOS)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT/backend"
FRONTEND_DIR="$ROOT/frontend"

echo "========================================="
echo " Система диспетчеризации транспорта"
echo "========================================="

check_cmd() {
  if ! command -v "$1" &>/dev/null; then
    echo "[ОШИБКА] '$1' не найден. $2"
    exit 1
  fi
}
check_cmd python3 "Установите Python 3.11+: https://python.org"
check_cmd node    "Установите Node.js 18+: https://nodejs.org"
check_cmd npm     "Установите Node.js 18+: https://nodejs.org"

VENV="$BACKEND_DIR/.venv"
# Если venv существует, но это Windows-версия (нет bin/python) - пересоздаём
if [ -d "$VENV" ] && [ ! -f "$VENV/bin/python" ]; then
  echo "[!] Обнаружен Windows venv, пересоздаём для Linux..."
  rm -rf "$VENV"
fi

if [ ! -d "$VENV" ]; then
  echo "[1/4] Создаём виртуальное окружение Python..."
  python3 -m venv "$VENV"
fi

[ ! -f "$BACKEND_DIR/.env" ]  && cp "$BACKEND_DIR/.env.example"  "$BACKEND_DIR/.env"
[ ! -f "$FRONTEND_DIR/.env" ] && cp "$FRONTEND_DIR/.env.example" "$FRONTEND_DIR/.env"

echo "[2/4] Устанавливаем Python зависимости..."
source "$VENV/bin/activate"
pip install --upgrade pip -q
pip install -r "$BACKEND_DIR/requirements.txt" -q
echo "    Готово."

echo "[3/4] Запускаем бэкенд → http://127.0.0.1:8001 ..."
cd "$BACKEND_DIR"
python main.py &
BACKEND_PID=$!
cd "$ROOT"

echo "    Ожидаем запуска..."
for i in $(seq 1 20); do
  sleep 1
  if curl -s http://127.0.0.1:8001/health >/dev/null 2>&1; then
    echo "    Бэкенд запущен!"; break
  fi
done
echo ""

echo "[4/4] Запускаем фронтенд → http://localhost:3000 ..."
cd "$FRONTEND_DIR"
npm install -q
npm run dev &
FRONTEND_PID=$!
cd "$ROOT"

echo ""
echo "========================================="
echo "  Приложение: http://localhost:3000"
echo "  API Docs:   http://127.0.0.1:8001/docs"
echo ""
echo "  Демо-аккаунты (пароль: admin123):"
echo "   dispatcher / employee1 / driver1"
echo "  Ctrl+C для остановки"
echo "========================================="

cleanup() { kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0; }
trap cleanup INT TERM
wait
