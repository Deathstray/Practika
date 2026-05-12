# Система диспетчеризации служебного транспорта

Веб-приложение для управления заявками на служебный транспорт.

## Быстрый старт

### Требования

| Инструмент | Версия | Скачать |
|-----------|--------|---------|
| Python | 3.11+ | https://python.org |
| Node.js | 18+ | https://nodejs.org |

> Docker **не нужен** — приложение использует SQLite и запускается напрямую.

### Запуск (Windows)

```
Двойной клик на run-local.bat
```

Откроются два окна — бэкенд и фронтенд. Дождитесь их запуска (~1 мин) и откройте:

**http://localhost:3000**

### Запуск (Linux / macOS)

```bash
chmod +x run-local.sh
./run-local.sh
```

---

## Демо-аккаунты

Пароль для всех: **admin123**

| Логин | Роль |
|-------|------|
| `dispatcher` | Диспетчер |
| `employee1` | Сотрудник |
| `driver1` | Водитель |

---

## Адреса после запуска

| Сервис | URL |
|--------|-----|
| Приложение | http://localhost:3000 |
| API (Swagger) | http://127.0.0.1:8001/docs |

---

## Стек

- **Фронтенд**: Nuxt 3 + Vue 3 + Tailwind CSS + ECharts
- **Бэкенд**: FastAPI (Python 3.11)
- **БД**: SQLite (файл `backend/data/transport_db.sqlite3`, создаётся автоматически)
- **Авторизация**: JWT (python-jose + bcrypt)

---

## Структура проекта

```
Practika/
├── run-local.bat         ← запуск на Windows
├── run-local.sh          ← запуск на Linux/macOS
├── docker-compose.yml    ← опциональный Docker-запуск
├── backend/
│   ├── main.py           ← точка входа FastAPI
│   ├── models.py         ← SQLAlchemy модели
│   ├── schemas.py        ← Pydantic схемы
│   ├── auth.py           ← JWT утилиты
│   ├── seed.py           ← начальные данные
│   ├── config.py         ← настройки
│   ├── database.py       ← подключение SQLite
│   ├── requirements.txt
│   └── routers/
│       ├── auth.py       ← /auth/login, /register, /me
│       ├── drivers.py    ← /drivers CRUD
│       ├── vehicles.py   ← /vehicles CRUD
│       ├── orders.py     ← полный цикл заявок
│       └── extra.py      ← /addresses, /stats
└── frontend/
    ├── nuxt.config.ts
    ├── pages/
    │   ├── login.vue / register.vue
    │   ├── dispatcher/   ← дашборд, заявки, история, статистика
    │   ├── employee/     ← список заявок, форма новой
    │   └── driver/       ← назначенные поездки
    ├── layouts/          ← сайдбары для каждой роли
    └── components/       ← StatusBadge и др.
```

---

## Этапы практики

| Этапы | Оценка |
|-------|--------|
| 1–3 | 3 (удовлетворительно) |
| 1–4 | 4 (хорошо) |
| 1–5 | 5 (отлично) |

Реализованы все 5 этапов:
1. Фундамент — авторизация, JWT, CRUD справочников ✓
2. Заявки — создание, очередь диспетчера, принятие/отклонение ✓
3. Полный цикл — назначение, проверка занятости, водитель ✓
4. История, адреса с автодополнением, экспорт Excel ✓
5. Дашборд, статистика с ECharts-графиками ✓
