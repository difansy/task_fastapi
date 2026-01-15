## Афанасьев Дмитрий Павлович 5132704/30801

# Students API

## Описание

FastAPI-проект с API для студентов и групп. Все эндпоинты из задания реализованы. Данные в PostgreSQL (Docker). Слои разделены: models, schemas, services, api.

## Требования

- Python 3.11+
- Docker Compose
- Библиотеки: `requirements.txt`

## Установка

1. Скопируйте `.env.example` в `.env`.
2. Запустите: `docker-compose up --build`.
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
3. Очистка: `docker-compose down -v`.

## Эндпоинты (/api/v1/)

**Студенты:**
- POST /students/ — Создать ({name: str, age: int})
- GET /students/{id} — Получить по ID
- GET /students/ — Список 
- DELETE /students/{id} — Удалить
- POST /students/{id}/groups/{group_id} — Добавить в группу
- DELETE /students/{id}/group — Удалить из группы
- POST /students/{id}/move/{new_group_id} — Перевести в группу

**Группы:**
- POST /groups/ — Создать ({name: str})
- GET /groups/{id} — Получить по ID (с студентами)
- GET /groups/ — Список (с студентами)
- DELETE /groups/{id} — Удалить

## Структура

- app/core/config.py — Настройки
- app/db/ — БД (SQLAlchemy)
- app/models/ — Модели
- app/schemas/ — Pydantic
- app/services/ — Логика
- app/api/v1/ — Эндпоинты
- app/main.py — Запуск
- docker-compose.yml — Docker
- requirements.txt — Библиотеки

## Тестирование

В /docs протестируйте эндпоинты. 
