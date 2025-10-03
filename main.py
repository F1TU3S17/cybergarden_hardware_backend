from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.devices import router as devices_router
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events: выполняется при старте и завершении приложения"""
    # Startup: инициализация БД
    init_db()
    print("✅ Database initialized (tables created if not exist)")
    yield
    # Shutdown: здесь можно закрыть соединения, если нужно
    print("👋 Application shutdown")


app = FastAPI(title="Hack Backend", lifespan=lifespan)
app.include_router(devices_router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok"}

