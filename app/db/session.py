"""Управление сессиями базы данных и инициализация.

Этот модуль содержит настройки SQLAlchemy для подключения к базе данных,
создание сессий и управление схемой базы данных.

Components:
    - engine: SQLAlchemy engine для подключения к БД
    - SessionLocal: Фабрика сессий для работы с БД
    - Base: Базовый класс для всех ORM моделей
    - get_db(): FastAPI dependency для получения сессии БД
    - init_db(): Функция инициализации схемы БД
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# SQLAlchemy engine и базовый класс
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
"""SQLAlchemy engine для подключения к базе данных.

Настройка check_same_thread=False необходима для SQLite,
чтобы позволить использование соединения в разных потоках в FastAPI.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Фабрика сессий SQLAlchemy.

Создает новые сессии базы данных с отключенным autocommit и autoflush
для явного управления транзакциями.
"""

Base = declarative_base()
"""Базовый класс для всех ORM моделей.

Все модели базы данных должны наследоваться от этого класса.
"""


def get_db():
    """
    FastAPI dependency для получения сессии базы данных.
    
    Создает новую сессию для каждого запроса и гарантирует ее закрытие
    после завершения обработки запроса.
    
    Yields:
        Session: Сессия SQLAlchemy для работы с базой данных
        
    Example:
        >>> from fastapi import Depends
        >>> from app.db.session import get_db
        >>> 
        >>> @app.get("/items")
        >>> def get_items(db: Session = Depends(get_db)):
        ...     return db.query(Item).all()
        
    Note:
        Использует context manager для гарантированного закрытия сессии
        даже в случае исключений.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Инициализация базы данных - создание всех таблиц.
    
    Создает все таблицы, определенные в моделях, если они еще не существуют.
    Вызывается при запуске приложения или из скрипта инициализации.
    
    Example:
        >>> from app.db.session import init_db
        >>> init_db()
        >>> print("Таблицы созданы!")
        
    Note:
        Важно убедиться, что все модели импортированы до вызова этой функции,
        чтобы они были зарегистрированы в Base.metadata.
    """
    from app import models  # Убедитесь, что модели импортированы, чтобы они зарегистрировались в Base

    Base.metadata.create_all(bind=engine)
