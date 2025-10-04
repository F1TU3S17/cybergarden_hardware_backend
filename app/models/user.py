"""Модели пользователей системы.

Этот модуль содержит модели для работы с пользователями,
включая SQLAlchemy модель для базы данных и Pydantic схемы для валидации.

Классы:
    - User: SQLAlchemy модель пользователя в базе данных
    - BaseUser: Базовая Pydantic схема с основными полями
    - CreateUser: Pydantic схема для создания нового пользователя
"""

from typing import Optional
from pydantic import BaseModel
from app.api.enums.user_roles import UserRole
from app.models.base import Base, Column, String, DateTime, datetime, timezone, gen_id, gen_uuid, gen_uuid


class BaseUser(BaseModel):
    """Базовая схема пользователя для валидации данных.
    
    Содержит минимальный набор полей для аутентификации пользователя.
    
    Attributes:
        username (str): Имя пользователя (логин)
        password (str): Пароль в открытом виде (будет хеширован)
    """
    username: str
    password: str


class CreateUser(BaseUser):
    """Схема для создания нового пользователя.
    
    Расширяет BaseUser добавлением роли пользователя.
    Используется при регистрации новых пользователей в системе.
    
    Attributes:
        username (str): Уникальное имя пользователя
        password (str): Пароль (будет хеширован перед сохранением)
        role (UserRole): Роль пользователя (admin, worker)
        
    Example:
        >>> user_data = CreateUser(
        ...     username="john_doe",
        ...     password="secure_password",
        ...     role=UserRole.ADMIN
        ... )
    """
    username: str
    password: str
    role: UserRole


class User(Base):
    """Модель пользователя в базе данных.
    
    Представляет пользователя системы с аутентификацией и авторизацией.
    Содержит хешированный пароль для безопасного хранения учетных данных.
    
    Attributes:
        id (str): Уникальный идентификатор пользователя (генерируется автоматически)
        username (str): Уникальное имя пользователя для входа
        password_hash (str): Хешированный пароль (SHA-256)
        role (str): Роль пользователя (admin, worker)
        created_at (datetime): Дата и время создания аккаунта
        
    Methods:
        verify_password(password): Проверка правильности пароля
        
    Example:
        >>> user = User(
        ...     username="john_doe",
        ...     password_hash="hashed_password",
        ...     role="admin"
        ... )
        >>> db.add(user)
        >>> db.commit()
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def verify_password(self, password: str) -> bool:
        """Проверка соответствия пароля хешу.
        
        Сравнивает предоставленный пароль с сохраненным хешем.
        
        Args:
            password (str): Пароль в открытом виде для проверки
            
        Returns:
            bool: True если пароль совпадает, False в противном случае
            
        Note:
            Это упрощенная реализация. В production следует использовать
            bcrypt или passlib для безопасной проверки паролей.
        """
        # Here you would implement proper password hashing and verification
        return self.password_hash == password  # Simplified for example purposes


__all__ = ["User"]


