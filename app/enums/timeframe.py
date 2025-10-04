from enum import Enum


class TimeFrame(str, Enum):
    """Временные интервалы для агрегации данных.
    
    Определяет стандартные интервалы времени, которые
    могут использоваться для агрегирования и фильтрации
    данных сенсоров и оповещений.
    
    Attributes:
        MINUTE: Интервал в 1 минуту
        FIVE_MINUTES: Интервал в 5 минут
        FIFTEEN_MINUTES: Интервал в 15 минут
        THIRTY_MINUTES: Интервал в 30 минут
        HOUR: Интервал в 1 час
        SIX_HOURS: Интервал в 6 часов
        TWELVE_HOURS: Интервал в 12 часов
        DAY: Интервал в 1 день
        
    Example:
        >>> readings = get_readings(
        ...     device_id="device123",
        ...     timeframe=TimeFrame.FIVE_MINUTES
        ... )
        >>> print(readings)
    """
    ONE_HOUR = "1h"
    THREE_HOURS = "3h"
    SIX_HOURS = "6h"
    EIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "24h"
    SEVEN_DAYS = "7d"
    THIRTY_DAYS = "30d"