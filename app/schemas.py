from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ChannelType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    TELEGRAM = "telegram"

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    telegram_id: Optional[str] = None
    priority_channel: ChannelType = ChannelType.EMAIL

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TemplateBase(BaseModel):
    name: str
    subject: str
    content: str
    channel_type: ChannelType

class TemplateCreate(TemplateBase):
    pass

class Template(TemplateBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    user_id: int
    template_id: int

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SendNotificationRequest(BaseModel):
    user_id: int
    template_name: str
    template_variables: Optional[dict] = None