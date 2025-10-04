"""
Hack Backend API Application
=============================

Главное приложение FastAPI для управления IoT устройствами, датчиками и оповещениями.

Основные возможности:
    - Управление устройствами (CRUD операции)
    - Мониторинг показаний датчиков
    - Система оповещений и алертов
    - Аутентификация и авторизация пользователей
    - Управление командами для устройств

Технологический стек:
    - FastAPI - веб-фреймворк
    - SQLAlchemy - ORM для работы с базой данных
    - SQLite - база данных (для разработки)

Запуск приложения:
    uvicorn main:app --reload --port 8000

API документация доступна по адресу:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from app.api.v1.devices import router as devices_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.commands import router as commands_router
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    
    Эта функция выполняется при запуске и завершении приложения FastAPI.
    Используется для инициализации ресурсов (база данных, соединения) 
    и их корректного освобождения при завершении работы.
    
    Args:
        app (FastAPI): Экземпляр приложения FastAPI
        
    Yields:
        None: Управление возвращается приложению для обработки запросов
        
    Lifecycle:
        - Startup: Инициализация базы данных, создание таблиц
        - Running: Приложение обрабатывает запросы
        - Shutdown: Освобождение ресурсов, закрытие соединений
    """
    # Startup: инициализация БД
    init_db()
    print("✅ Database initialized (tables created if not exist)")
    yield
    # Shutdown: здесь можно закрыть соединения, если нужно
    print("👋 Application shutdown")


# Инициализация FastAPI приложения
app = FastAPI(
    title="Hack Backend",
    description="API для управления IoT устройствами, мониторинга датчиков и системы оповещений",
    version="1.0.0",
    lifespan=lifespan
)

# Подключение роутеров API v1
app.include_router(devices_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(commands_router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
def html():
    return FileResponse('index.html')