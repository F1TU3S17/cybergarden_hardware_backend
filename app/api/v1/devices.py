from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.enums.device_status import DeviceStatus
from app.enums.sensor_type import SensorType
from app.enums.timeframe import TimeFrame
from app.db.session import get_db
from app.db.redis_client import RedisClient, get_redis
from app.models.device import Device
from app.models.device_limits import DeviceValues
from app.models.sensor_reading import ReadingBase, SensorReading
from app.models.alert import Alert
from app.models.command import Command


router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", status_code=201)
async def create_device(
    name: str,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Создать новое устройство.
    
    Пример запроса:
    POST /api/v1/devices?name=Sensor_001&location=Warehouse
    """
    device = Device(
        name=name,
        location=location,
        status="active"
    )
    db.add(device)
    db.commit()
    db.refresh(device)  # обновить объект с данными из БД (id, created_at)
    
    return device


@router.get("/")
async def get_all_devices(
    status: Optional[DeviceStatus] = Query(None, description="Фильтр по статусу"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Получить список всех устройств с фильтрацией.
    
    Примеры:
    GET /api/v1/devices
    GET /api/v1/devices?status=online&limit=5
    """
    query = db.query(Device)
    
    # Фильтрация
    if status:
        query = query.filter(Device.status == status)
    
    devices = query.limit(limit).all()

    count_readings = db.query(SensorReading).filter(SensorReading.device_id.in_([d.id for d in devices])).count()
    count_alerts = db.query(Alert).filter(Alert.device_id.in_([d.id for d in devices])).count()
    
    return {
        "total": len(devices),
        "count_total_readings": count_readings,
        "count_total_alerts": count_alerts,
        "devices": [
            {
                "id": d.id,
                "name": d.name,
                "location": d.location,
                "status": d.status,
                "last_seen": d.last_seen
            }
            for d in devices
        ]
    }


@router.get("/{device_id}")
async def get_device(device_id: str, db: Session = Depends(get_db)):
    """
    Получить устройство по ID со связанными данными.
    
    Пример:
    GET /api/v1/devices/550e8400-e29b-41d4-a716-446655440000
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Используем SQL запросы для подсчета вместо загрузки всех данных
    readings_count = db.query(SensorReading).filter(SensorReading.device_id == device_id).count()
    alerts_count = db.query(Alert).filter(Alert.device_id == device_id).count()
    commands_count = db.query(Command).filter(Command.device_id == device_id).count()
    
    return {
        'device': device,
        # Связанные данные через relationships
        "readings_count": readings_count,
        "alerts_count": alerts_count,
        "commands_count": commands_count
    }





@router.patch("/{device_id}")
async def update_device(
    device_id: str,
    status: Optional[DeviceStatus] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Обновить данные устройства.
    
    Пример:
    PATCH /api/v1/devices/{id}?status=maintenance&location=Lab
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Обновляем только переданные поля
    if status:
        device.status = status
    if location:
        device.location = location
    
    device.last_seen = datetime.now()
    
    
    db.commit()
    db.refresh(device)
    
    return device


# ============= DELETE (удаление) =============

@router.delete("/{device_id}")
async def delete_device(device_id: str, db: Session = Depends(get_db)):
    """
    Удалить устройство (и все связанные записи благодаря cascade).
    
    Пример:
    DELETE /api/v1/devices/{id}
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device_name = device.name
    db.delete(device)
    db.commit()
    
    return {"deleted": True, "name": device_name}


# ============= СВЯЗАННЫЕ ДАННЫЕ (relationships) =============

@router.post("/{device_id}/readings")
async def add_reading(
    create_reading: ReadingBase,
    db: Session = Depends(get_db)
):
    """
    Добавить показание датчика для устройства.
    
    Пример:
    POST /api/v1/devices/{id}/readings?sensor_type=temperature&value=23.5&unit=°C
    """
    # Проверить существование устройства
    device = db.query(Device).filter(Device.id == create_reading.device_id).first()
    print(create_reading)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    reading = SensorReading(
        device_id=create_reading.device_id,
        sensor_type=create_reading.sensor_type,
        value=create_reading.value,
        unit=create_reading.unit
    )
    db.add(reading)
    
    # Обновить last_seen устройства
    device.last_seen = datetime.now()
    
    db.commit()
    db.refresh(reading)
    
    return reading


@router.get("/{device_id}/readings")
async def get_device_readings(
    device_id: str,
    limit: int = Query(10, ge=1, le=1000),
    sensor_type: Optional[SensorType] = Query(None, description="Фильтр по типу датчика"),
    timeframe: Optional[TimeFrame] = Query(None, description="Временной интервал"),
    db: Session = Depends(get_db)
):
    """
    Получить последние показания датчиков устройства.
    
    Пример:
    GET /api/v1/devices/{id}/readings?limit=20
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Строим SQL запрос вместо загрузки всех данных в память
    query = db.query(SensorReading).filter(SensorReading.device_id == device_id)
    
    # Фильтр по типу датчика
    if sensor_type:
        query = query.filter(SensorReading.sensor_type == sensor_type)

    # Фильтр по времени
    if timeframe:
        time_delta = None
        match timeframe:
            case TimeFrame.ONE_HOUR:
                time_delta = timedelta(hours=1)
            case TimeFrame.THREE_HOURS:
                time_delta = timedelta(hours=3)
            case TimeFrame.SIX_HOURS:
                time_delta = timedelta(hours=6)
            case TimeFrame.EIGHT_HOURS:
                time_delta = timedelta(hours=8)
            case TimeFrame.TWELVE_HOURS:
                time_delta = timedelta(hours=12)
            case TimeFrame.ONE_DAY:
                time_delta = timedelta(days=1)
            case TimeFrame.SEVEN_DAYS:
                time_delta = timedelta(days=7)
            case TimeFrame.THIRTY_DAYS:
                time_delta = timedelta(days=30)
            case _:
                raise HTTPException(status_code=400, detail="Invalid timeframe")
        
        if time_delta:
            cutoff_time = datetime.now() - time_delta
            query = query.filter(SensorReading.timestamp >= cutoff_time)

    # Получаем общее количество записей (без limit)
    total_count = query.count()
    
    # Сортируем по времени (последние первыми) и применяем limit
    readings = query.order_by(SensorReading.timestamp.desc()).limit(limit).all()

    return {
        "device_id": device_id,
        "device_name": device.name,
        "total": total_count,
        "returned": len(readings),
        "readings": [
            {
                "id": r.id,
                "sensor_type": r.sensor_type,
                "value": r.value,
                "unit": r.unit,
                "timestamp": r.timestamp
            }
            for r in readings
        ]
    }


@router.post("/{device_id}/values", status_code=200)
async def set_device_values(
    values: DeviceValues,
    db: Session = Depends(get_db),
    redis: RedisClient = Depends(get_redis)
):
    """
    Установить значения устройства в Redis.
    
    Значения сохраняются в Redis для быстрого доступа и используются
    устройствами для получения текущих настроек.
    """
    # Проверяем существование устройства в БД
    device = db.query(Device).filter(Device.id == values.device_id).first()
  
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Формируем словарь только с переданными значениями
    device_values = {}
    if values.temperature_limit is not None:
        device_values["temperature_limit"] = values.temperature_limit
    if values.humidity_limit is not None:
        device_values["humidity_limit"] = values.humidity_limit
    if values.fire_limit is not None:
        device_values["fire_limit"] = values.fire_limit
    if values.servo_position is not None:
        device_values["servo_position"] = values.servo_position

    # Сохраняем в Redis
    success = redis.set_device_values(values.device_id, device_values)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save device values to Redis")
    
    return {
        "success": True,
        "device_id": values.device_id,
        "values": device_values,
        "message": "Device values successfully saved to Redis"
    }


@router.get("/{device_id}/values", status_code=200)
async def get_device_values(
    device_id: str,
    db: Session = Depends(get_db),
    redis: RedisClient = Depends(get_redis)
):
    """
    Получить текущие значения устройства из Redis.
    
    Возвращает все сохраненные настройки устройства (лимиты и позиции).
    
    Example:
        GET /api/v1/devices/550e8400-e29b-41d4-a716-446655440000/values
        
        Response:
        {
            "device_id": "550e8400-e29b-41d4-a716-446655440000",
            "device_name": "Sensor_001",
            "values": {
                "temperature_limit": 25.0,
                "humidity_limit": 60.0,
                "fire_limit": 100.0,
                "servo_position": 90
            }
        }
    """
    # Проверяем существование устройства в БД
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Получаем значения из Redis
    device_values = redis.get_device_values(device_id)
    
    if device_values is None:
        # Если в Redis нет данных, возвращаем пустой объект
        device_values = {}
    
    return {
        "device_id": device_id,
        "device_name": device.name,
        "values": device_values
    }
