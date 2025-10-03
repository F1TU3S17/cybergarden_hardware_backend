from pydantic import BaseModel
from app.api.enums.sensor_type import SensorType
from app.models.base import Base, Column, String, Float, DateTime, ForeignKey, datetime, gen_id, relationship


class ReadingBase(BaseModel):
    device_id: str
    sensor_type: SensorType
    value: float
    unit: str


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    sensor_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now())

    device = relationship("Device", back_populates="readings")


__all__ = ["SensorReading"]
