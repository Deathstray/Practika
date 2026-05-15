import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from database import engine
from models import Base
from routers.auth import router as auth_router
from routers.drivers import router as drivers_router
from routers.vehicles import router as vehicles_router
from routers.orders import router as orders_router
from routers.extra import addr_router, stats_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём таблицы один раз при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Система диспетчеризации служебного транспорта",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Глобальный обработчик ошибок ─────────────────────────────────────────────

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(f"IntegrityError: {exc}")
    return JSONResponse(
        status_code=409,
        content={"detail": "Конфликт данных: запись уже существует или нарушено ограничение целостности."},
    )

@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера. Попробуйте позже."},
    )

# ── Роутеры ───────────────────────────────────────────────────────────────────

app.include_router(auth_router)
app.include_router(drivers_router)
app.include_router(vehicles_router)
app.include_router(orders_router)
app.include_router(addr_router)
app.include_router(stats_router)


@app.get("/health")
def health():
    return {"status": "ok"}
