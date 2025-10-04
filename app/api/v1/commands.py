
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.enums.action_type import ActionType
from app.db.session import get_db
from app.enums.command_status import CommandStatus
from app.models.command import Command, CreateCommand, UpdateCommandStatus
from app.models.device import Device


router = APIRouter(prefix="/device/commands", tags=["commands"])

@router.post("/", status_code=201)
async def create_command(
    create_command: CreateCommand,
    db: Session = Depends(get_db)
):
    """
    Создать новую команду для устройства.
    """
    device = db.query(Device).filter(Device.id == create_command.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    command = Command(
        device_id=create_command.device_id,
        action=create_command.action,
        value=create_command.value,
        status=CommandStatus.PENDING
    )
    db.add(command)
    db.commit()
    db.refresh(command) 
    
    return command

@router.get('/{device_id}/{command_status}', status_code=200)
async def get_device_commands_list(device_id: str, command_status: CommandStatus = CommandStatus.PENDING,  db: Session = Depends(get_db)):
    """
    Получить список команд, которые отсносятся к устройству
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    commands = db.query(Command).filter((Command.device_id == device_id) & (Command.status == command_status)).all()

    return commands

@router.put('/status', status_code=200)
async def update_command_status(update_command_status: UpdateCommandStatus, db: Session = Depends(get_db)):
    """
    Обновить статус комманды девайса 
    """
    device = db.query(Device).filter(Device.id == update_command_status.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    command = db.query(Command).filter(Command.id == update_command_status.command_id).first()
    if not command:
        raise HTTPException(status_code=404, detail="Command not found")
    
    command.status = update_command_status.new_status
    
    db.add(command)
    db.commit()
    db.refresh(command)

    return command


    

    
