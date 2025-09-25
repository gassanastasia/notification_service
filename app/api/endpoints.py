from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas, crud

router = APIRouter()

@router.post("/send", response_model=schemas.Notification)
async def send_notification(
    request: schemas.SendNotificationRequest, 
    db: Session = Depends(get_db)
):
    # Проверяем существование пользователя
    user = crud.get_user(db, request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Получаем шаблон
    template = crud.get_template_by_name(db, request.template_name)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Создаем запись уведомления
    notification_data = schemas.NotificationCreate(
        user_id=request.user_id,
        template_id=template.id
    )
    notification = crud.create_notification(db, notification_data)
    
    # TODO: Здесь будет логика отправки через Celery
    # send_notification_task.delay(notification.id)
    
    return notification

@router.get("/notifications", response_model=List[schemas.Notification])
def get_notifications(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    notifications = crud.get_notifications(db, skip=skip, limit=limit)
    return notifications

@router.get("/users", response_model=List[schemas.User])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)