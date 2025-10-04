from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db

from app.enums.alert_status import AlertStatus
from app.models.user import BaseUser, CreateUser, User
from app.service.password_service import PasswordService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    login_user: BaseUser,
    db: Session = Depends(get_db)
):
    """
    Аутентификация пользователя.

    """
    user = db.query(User).filter(User.username == login_user.username).first()
    if not user or not PasswordService.verify_password(login_user.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Здесь можно добавить генерацию и возврат JWT токена или сессии
    return {"message": "Login successful", "status": "authenticated"}

@router.post("/register", status_code=201)
def register(
    create_user: CreateUser,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя.

    """
    existing_user = db.query(User).filter(User.username == create_user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = User(
        username=create_user.username,
        role=create_user.role,
        password_hash=PasswordService.hash_password(create_user.password)   
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # обновить объект с данными из БД (id, created_at)
    
    return user