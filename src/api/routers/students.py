"""
API Роутер для работы со студентами
Обрабатывает HTTP запросы, связанные со студентами
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_async_session
from src.repositories.repositories import StudentRepository
from src.services.services import StudentService
from src.schemas.schemas import StudentCreate, StudentResponse, StudentWithGroups

router = APIRouter()


async def get_student_service(session: AsyncSession = Depends(get_async_session)) -> StudentService:
    """
    Dependency для получения сервиса студентов
    Создаёт репозиторий и сервис с текущей сессией БД
    """
    repository = StudentRepository(session)
    return StudentService(repository)


@router.post("/students", response_model=StudentResponse, status_code=201)
async def create_student(
        student_data: StudentCreate,
        service: StudentService = Depends(get_student_service)
):
    """
    Создать нового студента

    - **first_name**: Имя студента
    - **last_name**: Фамилия студента
    - **email**: Email студента (должен быть уникальным)
    """
    try:
        student = await service.create_student(student_data)
        return student
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/students/{student_id}", response_model=StudentWithGroups)
async def get_student(
        student_id: int,
        service: StudentService = Depends(get_student_service)
):
    """
    Получить информацию о студенте по его ID

    Возвращает студента со списком его групп
    """
    try:
        student = await service.get_student(student_id)
        return student
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/students", response_model=list[StudentWithGroups])
async def get_all_students(
        service: StudentService = Depends(get_student_service)
):
    """
    Получить список всех студентов

    Возвращает всех студентов с их группами
    """
    students = await service.get_all_students()
    return students


@router.delete("/students/{student_id}")
async def delete_student(
        student_id: int,
        service: StudentService = Depends(get_student_service)
):
    """
    Удалить студента по ID

    При удалении студент автоматически удаляется из всех групп
    """
    try:
        result = await service.delete_student(student_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))