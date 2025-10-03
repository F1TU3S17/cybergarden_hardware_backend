from pydantic import BaseModel
from app.api.enums.alert_type import AlertType
from app.models.base import Base, Column, String, Boolean, DateTime, ForeignKey, Text, datetime, gen_id, relationship


class BaseAlert(BaseModel):
    device_id: str
    message: str
    severity: str
    alert_type: AlertType


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    alert_type = Column(String, nullable=True)  # Тип оповещения
    code = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    severity = Column(String, nullable=True)  # Уровень важности (low, medium, high, critical)
    status = Column(String, nullable=True)  # Статус оповещения (new, in_progress, resolved, etc.)
    acknowledged = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.now())

    device = relationship("Device", back_populates="alerts")


__all__ = ["Alert"]
