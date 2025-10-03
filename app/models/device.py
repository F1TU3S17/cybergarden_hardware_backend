from app.models.base import Base, Column, String, DateTime, JSON, datetime, gen_id, relationship


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    status = Column(String, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    readings = relationship("SensorReading", back_populates="device", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")
    commands = relationship("Command", back_populates="device", cascade="all, delete-orphan")


__all__ = ["Device"]
