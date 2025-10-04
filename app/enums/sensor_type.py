"""Перечисление типов датчиков.

Этот модуль определяет типы датчиков, которые могут быть
подключены к IoT устройствам и передавать данные.

Enums:
    SensorType: Типы датчиков, поддерживаемых системой
"""

from enum import Enum


class SensorType(str, Enum):
    """Типы датчиков, поддерживаемых системой.
    
    Определяет виды датчиков, которые могут передавать
    показания в систему мониторинга.
    
    Attributes:
        TEMPERATURE: Датчик температуры (°C, °F, K)
        HUMIDITY: Датчик влажности (%)
        ALERT: Датчик тревоги/оповещений (бинарное значение)
        
    Example:
        >>> reading = SensorReading(
        ...     sensor_type=SensorType.TEMPERATURE,
        ...     value=23.5,
        ...     unit="°C"
        ... )
        >>> print(reading.sensor_type.value)
        'temperature'
        
    Note:
        При добавлении новых типов датчиков необходимо обновить
        этот enum и соответствующую логику обработки.
    """
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    ALERT = "alert"
    FIRE = "fire"