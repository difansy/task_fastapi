"""
API Роутер для работы с группами
Обрабатывает HTTP запросы, связанные с группами и операциями со студентами
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_async_session
from src.repositories.repositories import GroupRepository
from src.services.services import GroupService
from src.schemas.schemas import (
    GroupCreate,
    GroupResponse,
    GroupWithStudents,
    AddStudentToGroup,
    TransferStudent,
    StudentResponse
)

router = APIRouter()


async def get_group_service(session: AsyncSession = Depends(get_async_session)) -> GroupService:
    """
    Dependency для получения сервиса групп
    Создаёт репозиторий и сервис с текущей сессией БД
    """
    repository = GroupRepository(session)
    return GroupService(repository)


@router.post("/groups", response_model=GroupResponse, status_code=201)
async def create_group(
        group_data: GroupCreate,
        service: GroupService = Depends(get_group_service)
):
    """
    Создать новую группу

    - **name**: Название группы (должно быть уникальным)
    - **description**: Описание группы (необязательно)
    """
    try:
        group = await service.create_group(group_data)
        return group
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/groups/{group_id}", response_model=GroupWithStudents)
async def get_group(
        group_id: int,
        service: GroupService = Depends(get_group_service)
):
    """
    Получить информацию о группе по её ID

    Возвращает группу со списком студентов
    """
    try:
        group = await service.get_group(group_id)
        return group
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/groups", response_model=list[GroupWithStudents])
async def get_all_groups(
        service: GroupService = Depends(get_group_service)
):
    """
    Получить список всех групп

    Возвращает все группы со списками студентов
    """
    groups = await service.get_all_groups()
    return groups


@router.delete("/groups/{group_id}")
async def delete_group(
        group_id: int,
        service: GroupService = Depends(get_group_service)
):
    """
    Удалить группу по ID

    При удалении группы студенты не удаляются, только связи
    """
    try:
        result = await service.delete_group(group_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/groups/add-student")
async def add_student_to_group(
        data: AddStudentToGroup,
        service: GroupService = Depends(get_group_service)
):
    """
    Добавить студента в группу

    - **student_id**: ID студента
    - **group_id**: ID группы

    Если студент уже в группе, ничего не произойдёт
    """
    try:
        result = await service.add_student_to_group(data.student_id, data.group_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/groups/remove-student")
async def remove_student_from_group(
        data: AddStudentToGroup,
        service: GroupService = Depends(get_group_service)
):
    """
    Удалить студента из группы

    - **student_id**: ID студента
    - **group_id**: ID группы
    """
    try:
        result = await service.remove_student_from_group(data.student_id, data.group_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/groups/{group_id}/students", response_model=list[StudentResponse])
async def get_group_students(
        group_id: int,
        service: GroupService = Depends(get_group_service)
):
    """
    Получить всех студентов в группе

    Возвращает список студентов без информации об их других группах
    """
    try:
        group = await service.get_group(group_id)
        return group.students
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/groups/transfer-student")
async def transfer_student(
        data: TransferStudent,
        service: GroupService = Depends(get_group_service)
):
    """
    Перевести студента из группы A в группу B

    - **student_id**: ID студента
    - **from_group_id**: ID группы, из которой переводим
    - **to_group_id**: ID группы, в которую переводим

    Студент удаляется из первой группы и добавляется во вторую
    """
    try:
        result = await service.transfer_student(
            data.student_id,
            data.from_group_id,
            data.to_group_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))