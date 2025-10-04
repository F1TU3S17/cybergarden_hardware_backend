from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.api.enums.sensor_type import SensorType
from app.api.enums.timeframe import TimeFrame
from app.db.session import get_db
from app.models.device import Device
from app.models.sensor_reading import ReadingBase, SensorReading


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
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
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
    
    return {
        "total": len(devices),
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
    
    # Используем relationships для получения связанных данных
    return {
        'device': device,
        # Связанные данные через relationships
        "readings_count": len(device.readings),
        "alerts_count": len(device.alerts),
        "commands_count": len(device.commands)
    }





@router.patch("/{device_id}")
async def update_device(
    device_id: str,
    status: Optional[str] = None,
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

    readings = device.readings[-limit:]  # последние N записей

    if timeframe:
        match timeframe:
            case TimeFrame.ONE_HOUR:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(hours=1)]
            case TimeFrame.THREE_HOURS:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(hours=3)]
            case TimeFrame.SIX_HOURS:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(hours=6)]
            case TimeFrame.TWELVE_HOURS:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(hours=12)]
            case TimeFrame.EIGHT_HOURS:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(hours=8)]
            case TimeFrame.ONE_DAY:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(days=1)]
            case TimeFrame.SEVEN_DAYS:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(days=7)]
            case TimeFrame.THIRTY_DAYS:
                readings = [r for r in readings if r.timestamp >= datetime.now() - timedelta(days=30)]
            case _:
                raise HTTPException(status_code=400, detail="Invalid timeframe")
        
    return {
        "device_id": device_id,
        "device_name": device.name,
        "total": len(readings),
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


