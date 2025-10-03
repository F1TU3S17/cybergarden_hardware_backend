from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models import Device, Alert, User
from app.api.enums.alert_status import AlertStatus
from app.service.password_service import PasswordService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    Аутентификация пользователя.
    
    Пример запроса:
    POST /api/v1/auth/login?username=johndoe&password=secret
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not PasswordService.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Здесь можно добавить генерацию и возврат JWT токена или сессии
    return {"message": "Login successful", "status": "authenticated"}

@router.post("/register", status_code=201)
def register(
    username: str,
    email: str,
    password: str,
    full_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя.
    
    Пример запроса:
    POST /
    """
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = User(
        username=username,
        email=email,
        full_name=full_name,
        password_hash=password  # Здесь нужно захешировать пароль
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # обновить объект с данными из БД (id, created_at)
    
    return user