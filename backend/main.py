from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from seed import seed
from routers.auth import router as auth_router
from routers.drivers import router as drivers_router
from routers.vehicles import router as vehicles_router
from routers.orders import router as orders_router
from routers.extra import addr_router, stats_router

seed()

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
