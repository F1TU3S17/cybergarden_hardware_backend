"""Redis client для работы с кэшем и временными данными.

Этот модуль предоставляет клиент Redis для хранения значений устройств,
кэширования и других операций с временными данными.
"""

import json
import redis
from typing import Optional, Dict, Any
from app.core.config import settings


class RedisClient:
    """Клиент для работы с Redis.
    
    Предоставляет методы для работы с device values и другими данными.
    """
    
    def __init__(self):
        """Инициализация подключения к Redis."""
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=settings.REDIS_DECODE_RESPONSES
        )
    
    def ping(self) -> bool:
        """Проверка подключения к Redis.
        
        Returns:
            bool: True если подключение успешно
        """
        try:
            return self.client.ping()
        except redis.ConnectionError:
            return False
    
    def set_device_values(self, device_id: str, values: Dict[str, Any], expire: Optional[int] = None) -> bool:
        """Сохранить значения устройства в Redis.
        
        Args:
            device_id: ID устройства
            values: Словарь со значениями (temperature_limit, humidity_limit, etc.)
            expire: Время жизни записи в секундах (None = без ограничения)
            
        Returns:
            bool: True если успешно сохранено
        """
        key = f"device:values:{device_id}"
        try:
            # Сохраняем как JSON строку
            self.client.set(key, json.dumps(values), ex=expire)
            return True
        except Exception as e:
            print(f"Error setting device values: {e}")
            return False
    
    def get_device_values(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Получить значения устройства из Redis.
        
        Args:
            device_id: ID устройства
            
        Returns:
            Dict со значениями или None если не найдено
        """
        key = f"device:values:{device_id}"
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error getting device values: {e}")
            return None
    
    def delete_device_values(self, device_id: str) -> bool:
        """Удалить значения устройства из Redis.
        
        Args:
            device_id: ID устройства
            
        Returns:
            bool: True если успешно удалено
        """
        key = f"device:values:{device_id}"
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Error deleting device values: {e}")
            return False
    
    def update_device_value(self, device_id: str, field: str, value: Any) -> bool:
        """Обновить одно поле в значениях устройства.
        
        Args:
            device_id: ID устройства
            field: Название поля (например, 'temperature_limit')
            value: Новое значение
            
        Returns:
            bool: True если успешно обновлено
        """
        try:
            current_values = self.get_device_values(device_id) or {}
            current_values[field] = value
            return self.set_device_values(device_id, current_values)
        except Exception as e:
            print(f"Error updating device value: {e}")
            return False
    
    def get_all_devices_with_values(self) -> Dict[str, Dict[str, Any]]:
        """Получить все устройства с их значениями.
        
        Returns:
            Dict где ключ - device_id, значение - словарь со значениями
        """
        result = {}
        try:
            # Ищем все ключи с паттерном device:values:*
            keys = self.client.keys("device:values:*")
            for key in keys:
                # Извлекаем device_id из ключа
                device_id = key.replace("device:values:", "")
                values = self.get_device_values(device_id)
                if values:
                    result[device_id] = values
            return result
        except Exception as e:
            print(f"Error getting all devices: {e}")
            return {}
    
    def close(self):
        """Закрыть подключение к Redis."""
        self.client.close()


# Глобальный экземпляр Redis клиента
redis_client = RedisClient()


def get_redis() -> RedisClient:
    """Dependency для получения Redis клиента в FastAPI endpoints.
    
    Returns:
        RedisClient: Экземпляр Redis клиента
        
    Example:
        @app.get("/test")
        async def test(redis: RedisClient = Depends(get_redis)):
            return {"ping": redis.ping()}
    """
    return redis_client
