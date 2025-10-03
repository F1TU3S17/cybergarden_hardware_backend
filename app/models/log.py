"""Модель логов для blockchain-подобного хранения данных устройств.

Этот модуль содержит модель для хранения логов устройств с криптографической
цепочкой, обеспечивающей целостность данных через хеширование и HMAC.

Classes:
    Log: SQLAlchemy модель лога с криптографической цепочкой
"""

from app.models.base import Base, Column, String, Integer, DateTime, ForeignKey, JSON, datetime, gen_id, relationship


class Log(Base):
    """Модель лога с криптографической цепочкой целостности.
    
    Представляет лог-запись устройства с blockchain-подобной структурой,
    где каждая запись содержит хеш предыдущей записи для обеспечения
    целостности цепочки данных.
    
    Attributes:
        id (str): Уникальный идентификатор лога
        device_id (str): ID устройства-источника (внешний ключ)
        seq (int, optional): Порядковый номер записи в цепочке
        timestamp (datetime): Дата и время создания записи
        type (str, optional): Тип лог-записи (data, event, command, etc.)
        sensors (JSON, optional): Данные датчиков в формате JSON
                                 Например: {"temp": 23.5, "humidity": 45}
        actions (JSON, optional): Выполненные действия в формате JSON
                                 Например: {"command": "restart", "status": "success"}
        prev_hash (str, optional): Хеш предыдущей записи в цепочке
        hash (str, optional): Хеш текущей записи (SHA-256)
        hmac (str, optional): HMAC подпись для проверки подлинности
        server_sig (str, optional): Серверная цифровая подпись
        
    Relationships:
        device (Device): Устройство, от которого получен лог
        
    Example:
        >>> log = Log(
        ...     device_id="abc123",
        ...     seq=42,
        ...     type="data",
        ...     sensors={"temperature": 23.5, "humidity": 45.2},
        ...     prev_hash="abc...def",
        ...     hash="def...ghi"
        ... )
        >>> db.add(log)
        >>> db.commit()
        
    Note:
        Структура логов позволяет обнаружить несанкционированные изменения
        путем проверки цепочки хешей. При изменении любой записи все
        последующие хеши станут невалидными.
    """
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
