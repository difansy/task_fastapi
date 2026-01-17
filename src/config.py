"""
Конфигурация приложения.
Загружает переменные окружения из .env файла
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения
    Автоматически загружаются из .env файла
    """
    # Параметры подключения к PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        """
        Формирует строку подключения к БД
        postgresql+asyncpg://user:password@host:port/database
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        # Имя файла с переменными окружения
        env_file = ".env"
        # Учитывать регистр букв в названиях переменных
        case_sensitive = True


settings = Settings()