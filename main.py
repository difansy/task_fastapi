import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.config import settings
from src.database.database import engine, Base, get_async_session
from src.models.models import Student, Group
from src.api.routers import students, groups

app = FastAPI(
    title="Students API",
    description="API для управления студентами и группами",
    version="1.0.0.0"
)


# Event handler для создания таблиц при старте приложения
@app.on_event("startup")
async def startup():
    """
    Выполняется при старте приложения
    Создаёт все таблицы в БД, если их нет
    """
    async with engine.begin() as conn:
        # Создаём все таблицы из моделей, наследующих Base
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована")


# Подключаем роутеры
app.include_router(students.router, prefix="/api/v1", tags=["students"])
app.include_router(groups.router, prefix="/api/v1", tags=["groups"])


@app.on_event("shutdown")
async def shutdown():
    """
    Выполняется при остановке приложения
    Корректно закрываем соединение с БД
    """
    await engine.dispose()
    print("Соединение с БД закрыто")


@app.get("/")
async def root():
    """
    Корневой эндпоинт
    Проверка работы API
    """
    return {
        "message": "Students API is running",
        "version": "1.0.0.0",
        "database_host": settings.POSTGRES_HOST,
        "database_name": settings.POSTGRES_DB
    }


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_async_session)):
    """
    Проверка здоровья приложения и подключения к БД
    """
    try:
        # Пробуем выполнить простой SQL запрос
        result = await session.execute(text("SELECT 1"))
        db_status = "connected" if result else "error"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status
    }


if __name__ == "__main__":
    # Запуск сервера
    # host="0.0.0.0" - доступен извне
    # port=8000 - порт
    # reload=True - перезагрузка при изменении кода
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )