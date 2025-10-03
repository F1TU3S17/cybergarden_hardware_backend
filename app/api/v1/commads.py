from click import Command
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models.device import Device


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