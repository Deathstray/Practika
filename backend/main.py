from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base
from routers.auth import router as auth_router
from routers.drivers import router as drivers_router
from routers.vehicles import router as vehicles_router
from routers.orders import router as orders_router
from routers.extra import addr_router, stats_router
from seed import seed_database


Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

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

app.include_router(auth_router)
app.include_router(drivers_router)
app.include_router(vehicles_router)
app.include_router(orders_router)
app.include_router(addr_router)
app.include_router(stats_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    from config import settings

    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=False,
    )
