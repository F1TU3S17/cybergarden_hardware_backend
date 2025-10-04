"""Модель устройства (IoT Device) для мониторинга и управления.

Этот модуль содержит SQLAlchemy модель для представления IoT устройств
в системе мониторинга, включая их статус, местоположение и связанные данные.

Classes:
    Device: Основная модель устройства с отношениями к показаниям, логам и алертам
"""

from app.models.base import Base, Column, String, DateTime, JSON, datetime, timezone, gen_id, relationship


class Device(Base):
    """Модель IoT устройства в системе.
    
    Представляет физическое или виртуальное устройство, подключенное к системе
    мониторинга. Содержит информацию о статусе, местоположении и связанных данных.
    
    Attributes:
        id (str): Уникальный идентификатор устройства (генерируется автоматически)
        name (str): Название устройства (обязательное поле)
        location (str, optional): Физическое расположение устройства
        status (str, optional): Текущий статус (active, offline, maintenance, etc.)
        last_seen (datetime, optional): Время последней активности устройства
        meta (JSON, optional): Дополнительные метаданные в формате JSON
        created_at (datetime): Дата и время регистрации устройства в системе
        
    Relationships:
        readings (List[SensorReading]): Показания датчиков от устройства
        logs (List[Log]): Логи активности устройства
        alerts (List[Alert]): Оповещения, связанные с устройством
        commands (List[Command]): Команды, отправленные устройству
        
    Cascade:
        При удалении устройства автоматически удаляются все связанные записи
        (readings, logs, alerts, commands) благодаря "all, delete-orphan"
        
    Example:
        >>> device = Device(
        ...     name="Temperature Sensor 01",
        ...     location="Warehouse A",
        ...     status="active",
        ...     meta={"model": "TMP36", "firmware": "1.2.3"}
        ... )
        >>> db.add(device)
        >>> db.commit()
    """
    __tablename__ = "devices"

    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    status = Column(String, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Отношения с каскадным удалением
    readings = relationship("SensorReading", back_populates="device", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")
    commands = relationship("Command", back_populates="device", cascade="all, delete-orphan")


__all__ = ["Device"]
