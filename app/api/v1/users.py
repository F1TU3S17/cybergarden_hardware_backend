from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models import User

router = APIRouter(prefix="/users", tags=["users"])

def get_user(db: Session, user_id: str):
    """Получить пользователя по ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=201)
def create_user(
    username: str,
    email: str,
    full_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Создать нового пользователя.
    
    Пример запроса:
    POST /
    """
    user = User(
        username=username,
        email=email,
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # обновить объект с данными из БД (id, created_at)
    
    return user

