from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models import Command, Device, SensorReading, Alert

router = APIRouter(prefix="/commands", tags=["commands"])

@router.post("/", status_code=201)

def create_command(
    device_id: str,
    command_type: str,
    parameters: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    """
    Создать новую команду для устройства.
    
    Пример запроса:
    POST /api/v1/commands?device_id=abc123&command_type=restart&parameters={"delay":5}
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    command = Command(
        device_id=device_id,
        command_type=command_type,
        parameters=parameters,
        status="pending"
    )
    db.add(command)
    db.commit()
    db.refresh(command)  # обновить объект с данными из БД (id, created_at)
    
    return command