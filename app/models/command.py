from app.models.base import Base, Column, String, DateTime, ForeignKey, JSON, datetime, gen_id, relationship


class Command(Base):
    __tablename__ = "commands"

    id = Column(String, primary_key=True, default=gen_id)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    action = Column(String, nullable=False)
    params = Column(JSON, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())

    device = relationship("Device", back_populates="commands")


__all__ = ["Command"]
