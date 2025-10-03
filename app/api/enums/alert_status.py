"""Перечисление статусов оповещений.

Этот модуль определяет возможные статусы жизненного цикла оповещения
от создания до закрытия.

Enums:
    AlertStatus: Статусы оповещений (NEW, IN_PROGRESS, RESOLVED, CLOSED)
"""

from enum import Enum


class AlertStatus(str, Enum):
    """Статусы оповещений в системе.
    
    Определяет этапы обработки оповещения от момента создания
    до окончательного закрытия.
    
    Attributes:
        NEW: Новое оповещение, требует внимания
        IN_PROGRESS: Оповещение в процессе обработки
        RESOLVED: Проблема решена, ожидает подтверждения
        CLOSED: Оповещение закрыто, работа завершена
        
    Example:
        >>> alert.status = AlertStatus.NEW
        >>> print(alert.status.value)
        'new'
        >>> alert.status = AlertStatus.IN_PROGRESS
    """
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"