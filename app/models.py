import random
import string
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Text,
)
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship

from app.db.session import Base


def gen_id():
    # Generate a simple random string ID
    ran = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return str(ran)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_id)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        # Here you would implement proper password hashing and verification
        return self.password_hash == password  # Simplified for example purposes
    


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


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    sensor_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now())

    device = relationship("Device", back_populates="readings")


class Log(Base):
    __tablename__ = "logs"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    seq = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.now())
    type = Column(String, nullable=True)
    sensors = Column(JSON, nullable=True)
    actions = Column(JSON, nullable=True)
    prev_hash = Column(String, nullable=True)
    hash = Column(String, nullable=True)
    hmac = Column(String, nullable=True)
    server_sig = Column(String, nullable=True)

    device = relationship("Device", back_populates="logs")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    code = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    acknowledged = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.now())

    device = relationship("Device", back_populates="alerts")


class Command(Base):
    __tablename__ = "commands"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    action = Column(String, nullable=False)
    params = Column(JSON, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())

    device = relationship("Device", back_populates="commands")
