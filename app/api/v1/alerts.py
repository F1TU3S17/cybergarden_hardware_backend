from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db

from app.enums.alert_status import AlertStatus
from app.models.alert import Alert, BaseAlert
from app.models.device import Device

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/", status_code=201)
async def create_alert(
    create_alert: BaseAlert,
    db: Session = Depends(get_db)
):
    """
    Создать новое оповещение для устройства.
    """
    device = db.query(Device).filter(Device.id == create_alert.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    alert = Alert(
        device_id=create_alert.device_id,
        alert_type=create_alert.alert_type,
        message=create_alert.message,
        severity=create_alert.severity,
        status=AlertStatus.NEW.value
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)  # обновить объект с данными из БД (id, created_at)
    
    return alert


@router.get("/{device_id}/alerts")
async def get_device_alerts(
    device_id: str,
    status: Optional[AlertStatus] = Query(None, description="Фильтр по статусу"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Получить список оповещений для устройства с фильтрацией.
    
    Примеры:
    GET /api/v1/alerts/abc123
    GET /api/v1/alerts/abc123?status=new&limit=5
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    query = db.query(Alert).filter(Alert.device_id == device_id)
    
    # Фильтрация
    if status:
        query = query.filter(Alert.status == status)
    
    alerts = query.order_by(Alert.timestamp.desc()).limit(limit).all()
    
    return {
        "device_id": device_id,
        "device_name": device.name,
        "total": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "alert_type": a.alert_type,
                "message": a.message,
                "severity": a.severity,
                "status": a.status,
                "timestamp": a.timestamp
            }
            for a in alerts
        ]
    }
    

@router.put("/{alert_id}/status")
async def update_alert_status(
    alert_id: str,
    status: AlertStatus,
    db: Session = Depends(get_db)
):
    """
    Обновить статус оповещения.
    
    Пример запроса:
    PUT /api/v1/alerts/alert123/status?status=resolved
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = status.value
    db.commit()
    db.refresh(alert)
    
    return alert