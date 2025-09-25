from fastapi import FastAPI
from app.database import engine, Base
from app.api.endpoints import router as api_router

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notification Service",
    description="Сервис для отправки уведомлений через Email, SMS, Telegram",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Notification Service API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}