"""Конфигурация приложения.

Этот модуль содержит настройки приложения, загружаемые из переменных окружения
или .env файла с использованием Pydantic BaseSettings.

Classes:
    Settings: Класс настроек приложения
    
Variables:
    settings: Глобальный экземпляр настроек
"""

from pydantic_settings import BaseSettings
import pytz

class Settings(BaseSettings):
    """Настройки приложения с загрузкой из переменных окружения.
    
    Наследуется от Pydantic BaseSettings для автоматической
    загрузки настроек из .env файла и переменных окружения.
    
    Attributes:
        PROJECT_NAME (str): Название проекта (по умолчанию "Hack Backend")
        DEBUG (bool): Режим отладки (по умолчанию True)
        DATABASE_URL (str): URL подключения к базе данных
                           (по умолчанию "sqlite:///./test.db")
        
    Config:
        env_file (str): Путь к .env файлу с настройками
        
    Example:
        .env файл:
        ```
        PROJECT_NAME="My IoT Project"
        DEBUG=False
        DATABASE_URL="postgresql://user:pass@localhost/dbname"
        ```
        
        Использование:
        >>> from app.core.config import settings
        >>> print(settings.PROJECT_NAME)
        "Hack Backend"
        >>> print(settings.DATABASE_URL)
        "sqlite:///./test.db"
        
    Note:
        В production используйте PostgreSQL или другую промышленную
        базу данных вместо SQLite.
    """
    PROJECT_NAME: str = "Hack Backend"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    AI_API_KEY: str  
    system_prompt: str = "You are a helpful assistant for analyzing IoT monitoring data. You will receive JSON data from various sensors and devices. Your task is to identify anomalies, trends, and potential issues based on the data provided. Provide clear, concise insights and recommendations for any detected problems. Send analytical situation and recommendations to the user. Response language is Russian."
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_DECODE_RESPONSES: bool = True


    class Config:
        """Конфигурация Pydantic Settings.
        
        Attributes:
            env_file (str): Путь к .env файлу
        """
        env_file = ".env"


# Глобальный экземпляр настроек
settings = Settings()
