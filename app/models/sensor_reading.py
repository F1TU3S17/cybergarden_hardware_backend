"""Модели показаний датчиков от IoT устройств.

Этот модуль содержит модели для работы с данными датчиков,
включая SQLAlchemy модель для базы данных и Pydantic схему для валидации.

Classes:
    SensorReading: SQLAlchemy модель показания датчика в базе данных
    ReadingBase: Pydantic схема для создания нового показания
"""

from pydantic import BaseModel
from app.api.enums.sensor_type import SensorType
from app.models.base import Base, Column, String, Float, DateTime, ForeignKey, datetime, gen_id, relationship


class ReadingBase(BaseModel):
    """Базовая схема показания датчика для валидации данных.
    
    Используется для валидации данных при создании новых показаний через API.
    
    Attributes:
        device_id (str): ID устройства, от которого получено показание
        sensor_type (SensorType): Тип датчика (temperature, humidity, alert)
        value (float): Числовое значение показания
        unit (str): Единица измерения (°C, %, lux, etc.)
        
    Example:
        >>> reading_data = ReadingBase(
        ...     device_id="abc123",
        ...     sensor_type=SensorType.TEMPERATURE,
        ...     value=23.5,
        ...     unit="°C"
        ... )
    """
    device_id: str
    sensor_type: SensorType
    value: float
    unit: str


class SensorReading(Base):
    """Модель показания датчика в базе данных.
    
    Представляет одно измерение, полученное от датчика IoT устройства.
    Хранит числовое значение, тип датчика, единицу измерения и временную метку.
    
    Attributes:
        id (str): Уникальный идентификатор показания
        device_id (str): ID устройства-источника (внешний ключ)
        sensor_type (str): Тип датчика (temperature, humidity, alert, etc.)
        value (float): Числовое значение показания (обязательное)
        unit (str, optional): Единица измерения (°C, %, Pa, lux, etc.)
        timestamp (datetime): Дата и время получения показания
        
    Relationships:
        device (Device): Устройство, от которого получено показание
        
    Example:
        >>> reading = SensorReading(
        ...     device_id="abc123",
        ...     sensor_type="temperature",
        ...     value=23.5,
        ...     unit="°C"
        ... )
        >>> db.add(reading)
        >>> db.commit()
        
    Note:
        Показания обычно создаются в больших количествах.
        Рассмотрите использование bulk_insert_mappings() для оптимизации.
    """
    __tablename__ = "sensor_readings"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    sensor_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now())

    device = relationship("Device", back_populates="readings")


__all__ = ["SensorReading"]
