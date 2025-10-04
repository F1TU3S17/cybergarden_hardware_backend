from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db

from app.enums.alert_status import AlertStatus
from app.enums.sensor_type import SensorType
from app.models.alert import Alert, BaseAlert
from app.models.device import Device
from app.models.sensor_reading import SensorReading
from app.service.gpt_service import GptService

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.post("/gpt/{device_id}", status_code=201)
async def analyze_data(
    device_id: str,
    db: Session = Depends(get_db)
):
    """
    Анализировать данные с помощью моделей GPT.
    """

    device = db.query(Device).filter(Device.id == device_id).first()
    sensor_readings = db.query(SensorReading).filter(
        SensorReading.device_id == device_id
    ).order_by(SensorReading.timestamp.desc()).limit(100).all()

    def serialize_reading(sr):
        return {
            "sensor_type": sr.sensor_type.value if hasattr(sr.sensor_type, 'value') else sr.sensor_type,
            "value": sr.value,
            "unit": sr.unit,
            "timestamp": sr.timestamp.isoformat() if sr.timestamp else None
        }
    
    fire_sensor_readings = [serialize_reading(sr) for sr in sensor_readings if sr.sensor_type == SensorType.FIRE]
    temperature_sensor_readings = [serialize_reading(sr) for sr in sensor_readings if sr.sensor_type == SensorType.TEMPERATURE]
    humidity_sensor_readings = [serialize_reading(sr) for sr in sensor_readings if sr.sensor_type == SensorType.HUMIDITY]
    
    gpt_service = GptService()

    data = {"device_id": device_id, "sensors": {"fire": fire_sensor_readings, "temperature": temperature_sensor_readings, "humidity": humidity_sensor_readings}} if device else {"error": "Device not found"}

    analysis_result = await gpt_service.analyze_monitoring_data(data)
    return {"message": "Data analyzed successfully", "analysis": analysis_result}