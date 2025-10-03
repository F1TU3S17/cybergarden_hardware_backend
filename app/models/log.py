from app.models.base import Base, Column, String, Integer, DateTime, ForeignKey, JSON, datetime, gen_id, relationship


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


__all__ = ["Log"]
