"""
Настройка подключения к базе данных.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

# Создаём асинхронный движок для работы с БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

# Фабрика для создания асинхронных сессий
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    """
    Базовый класс для ORM моделей
    Все модели будут наследоваться от него
    """
    pass


# Dependency для получения сессии БД в эндпоинтах
async def get_async_session():
    """
    Генератор для получения асинхронной сессии БД.
    Используется как зависимость в FastAPI эндпоинтах.
    """
    async with async_session_maker() as session:
        yield session