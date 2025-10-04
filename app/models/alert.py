"""Модели оповещений и алертов системы.

Этот модуль содержит модели для работы с оповещениями от IoT устройств,
включая SQLAlchemy модель для базы данных и Pydantic схему для валидации.

Classes:
    Alert: SQLAlchemy модель оповещения в базе данных
    BaseAlert: Pydantic схема для создания нового оповещения
"""

from pydantic import BaseModel
from app.api.enums.alert_type import AlertType
from app.models.base import Base, Column, String, Boolean, DateTime, ForeignKey, Text, datetime, timezone, gen_id, gen_uuid, relationship


class BaseAlert(BaseModel):
    """Базовая схема оповещения для валидации данных.
    
    Используется для создания новых оповещений через API.
    
    Attributes:
        device_id (str): ID устройства, от которого поступило оповещение
        message (str): Текст сообщения оповещения
        severity (str): Уровень важности (low, medium, high, critical)
        alert_type (AlertType): Тип оповещения (study, error, temperature, etc.)
    """
    device_id: str
    message: str
    severity: str
    alert_type: AlertType


class Alert(Base):
    """Модель оповещения в базе данных.
    
    Представляет оповещение или алерт от IoT устройства.
    Используется для уведомления о различных событиях: ошибках,
    превышении пороговых значений датчиков, и других важных событиях.
    
    Attributes:
        id (str): Уникальный идентификатор оповещения
        device_id (str): ID устройства-источника (внешний ключ)
        alert_type (str): Тип оповещения (temperature, humidity, motion, etc.)
        code (str, optional): Код ошибки или события
        message (Text, optional): Детальное описание оповещения
        severity (str, optional): Уровень важности (low, medium, high, critical)
        status (str, optional): Статус оповещения (new, in_progress, resolved, closed)
        acknowledged (bool): Подтверждено ли оповещение оператором (по умолчанию False)
        timestamp (datetime): Дата и время создания оповещения
        
    Relationships:
        device (Device): Устройство, от которого поступило оповещение
        
    Example:
        >>> alert = Alert(
        ...     device_id="abc123",
        ...     alert_type="temperature",
        ...     message="Temperature exceeded threshold",
        ...     severity="high",
        ...     status="new"
        ... )
        >>> db.add(alert)
        >>> db.commit()
    """
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=gen_uuid)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    alert_type = Column(String, nullable=True)  # Тип оповещения
    code = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    severity = Column(String, nullable=True)  # Уровень важности (low, medium, high, critical)
    status = Column(String, nullable=True)  # Статус оповещения (new, in_progress, resolved, etc.)
    acknowledged = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    device = relationship("Device", back_populates="alerts")


__all__ = ["Alert"]
