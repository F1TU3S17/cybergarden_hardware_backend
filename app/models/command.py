"""Модель команд для управления IoT устройствами.

Этот модуль содержит модель для представления команд,
отправляемых IoT устройствам для выполнения различных действий.

Classes:
    Command: SQLAlchemy модель команды в базе данных
"""

from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Numeric
from app.enums.action_type import ActionType
from app.enums.command_status import CommandStatus
from app.models.base import Base, Column, String, DateTime, ForeignKey, JSON, datetime, timezone, gen_id, relationship


class CreateCommand(BaseModel):
    device_id: str
    action: ActionType
    value: Optional[float] = None

class UpdateCommandStatus(BaseModel):
    device_id: str
    command_id: str
    new_status: CommandStatus
    

class Command(Base):
    """Модель команды для IoT устройства.
    
    Представляет команду, отправленную устройству для выполнения определенного действия.
    Отслеживает статус выполнения команды и параметры для её выполнения.
    
    Attributes:
        id (str): Уникальный идентификатор команды
        device_id (str): ID устройства-получателя (внешний ключ)
        action (str): Название действия/команды (обязательное поле)
                     Примеры: "restart", "update_config", "calibrate_sensor"
        params (JSON, optional): Параметры команды в формате JSON
                                Например: {"mode": "full", "delay": 30}
        status (str, optional): Статус выполнения (pending, in_progress, completed, failed)
        created_at (datetime): Дата и время создания команды
        
    Relationships:
        device (Device): Устройство, которому отправлена команда
        
    Example:
        >>> command = Command(
        ...     device_id="abc123",
        ...     action="restart",
        ...     params={"mode": "graceful", "delay": 5},
        ...     status="pending"
        ... )
        >>> db.add(command)
        >>> db.commit()
        
    Note:
        Команды обычно обрабатываются асинхронно. Устройство получает команду,
        обновляет статус по мере выполнения.
    """
    __tablename__ = "commands"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    action = Column(String, nullable=False)
    value = Column(Numeric, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now())

    device = relationship("Device", back_populates="commands")


__all__ = ["Command"]
