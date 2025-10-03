"""Перечисление типов оповещений.

Этот модуль определяет различные типы оповещений,
которые могут генерировать IoT устройства.

Enums:
    AlertType: Типы оповещений от устройств
"""

from enum import Enum


class AlertType(str, Enum):
    """Типы оповещений в системе мониторинга.
    
    Классифицирует оповещения по их природе и источнику.
    Используется для фильтрации и категоризации оповещений.
    
    Attributes:
        STUDY: Исследовательское оповещение, информационное сообщение
        ERROR: Ошибка устройства или системы
        TEMPERATURE: Оповещение, связанное с температурой
        HUMIDITY: Оповещение, связанное с влажностью
        MOTION: Обнаружение движения
        BATTERY: Оповещение о состоянии батареи
        
    Example:
        >>> alert = Alert(
        ...     alert_type=AlertType.TEMPERATURE,
        ...     message="Temperature exceeded 30°C"
        ... )
        >>> print(alert.alert_type.value)
        'temperature'
    """
    STUDY = "study"
    ERROR = "error"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    MOTION = "motion"
    BATTERY = "battery"
    