"""Базовые компоненты для моделей базы данных.

Этот модуль содержит общие импорты и утилиты для работы с SQLAlchemy моделями,
включая генераторы идентификаторов и базовые типы данных.

Компоненты:
    - Base: Базовый класс для всех SQLAlchemy моделей
    - gen_id(): Генератор коротких случайных ID
    - gen_uuid(): Генератор UUID идентификаторов
    - Типы колонок: Column, String, Integer, Float, Boolean, DateTime, и др.

Пример использования:
    >>> from app.models.base import Base, Column, String, gen_id
    >>>
    >>> class MyModel(Base):
    ...     __tablename__ = "my_table"
    ...     id = Column(String, primary_key=True, default=gen_id)
"""

import random
import string
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship

from app.db.session import Base


def gen_id() -> str:
    """Генерация короткого случайного идентификатора.
    
    Создает 4-символьную строку из букв (a-z, A-Z) и цифр (0-9).
    Используется для простых ID в таблицах базы данных.
    
    Returns:
        str: Случайная строка из 4 символов
        
    Example:
        >>> gen_id()
        'aB3d'
        >>> gen_id()
        'X9mK'
        
    Note:
        Не гарантирует уникальность. Для критичных систем используйте gen_uuid().
    """
    ran = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return str(ran)

def gen_uuid() -> str:
    """Генерация уникального идентификатора UUID.
    
    Создает UUID версии 4 (случайный) и преобразует его в строку.
    Обеспечивает высокую степень уникальности для идентификаторов.
    
    Returns:
        str: UUID в строковом формате (например: '550e8400-e29b-41d4-a716-446655440000')
        
    Example:
        >>> gen_uuid()
        '550e8400-e29b-41d4-a716-446655440000'
        
    Note:
        Гарантирует практически полную уникальность. Рекомендуется для production.
    """
    import uuid
    return str(uuid.uuid4())

__all__ = ["Base", "gen_id", "gen_uuid", "Column", "String", "Integer", "Float", "Boolean", 
           "DateTime", "ForeignKey", "JSON", "Text", "BLOB", "relationship", "datetime"]
