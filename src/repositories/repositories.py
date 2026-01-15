"""
Repository Layer - слой работы с базой данных
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.models.models import Student, Group


class StudentRepository:
    """Репозиторий для работы со студентами"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, first_name: str, last_name: str, email: str) -> Student:
        """
        Создать нового студента

        Args:
            first_name: Имя студента
            last_name: Фамилия студента
            email: Email студента

        Returns:
            Созданный объект Student
        """
        student = Student(first_name=first_name, last_name=last_name, email=email)
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)  # Обновляем объект с данными из БД (например, id)
        return student

    async def get_by_id(self, student_id: int) -> Student | None:
        """
        Получить студента по ID с его группами

        Args:
            student_id: ID студента

        Returns:
            Объект Student или None, если не найден
        """
        stmt = select(Student).where(Student.id == student_id).options(selectinload(Student.groups))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Student]:
        """
        Получить всех студентов с их группами

        Returns:
            Список объектов Student
        """
        stmt = select(Student).options(selectinload(Student.groups))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, student_id: int) -> bool:
        """
        Удалить студента по ID

        Args:
            student_id: ID студента

        Returns:
            True если удалён, False если не найден
        """
        student = await self.get_by_id(student_id)
        if student:
            await self.session.delete(student)
            await self.session.commit()
            return True
        return False


class GroupRepository:
    """Репозиторий для работы с группами"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, description: str | None = None) -> Group:
        """
        Создать новую группу

        Args:
            name: Название группы
            description: Описание группы (необязательно)

        Returns:
            Созданный объект Group
        """
        group = Group(name=name, description=description)
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group

    async def get_by_id(self, group_id: int) -> Group | None:
        """
        Получить группу по ID со списком студентов

        Args:
            group_id: ID группы

        Returns:
            Объект Group или None, если не найдена
        """
        stmt = select(Group).where(Group.id == group_id).options(selectinload(Group.students))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Group]:
        """
        Получить все группы со списками студентов

        Returns:
            Список объектов Group
        """
        stmt = select(Group).options(selectinload(Group.students))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, group_id: int) -> bool:
        """
        Удалить группу по ID

        Args:
            group_id: ID группы

        Returns:
            True если удалена, False если не найдена
        """
        group = await self.get_by_id(group_id)
        if group:
            await self.session.delete(group)
            await self.session.commit()
            return True
        return False

    async def add_student_to_group(self, student_id: int, group_id: int) -> bool:
        """
        Добавить студента в группу

        Args:
            student_id: ID студента
            group_id: ID группы

        Returns:
            True если добавлен, False если студент или группа не найдены
        """
        group = await self.get_by_id(group_id)
        student_repo = StudentRepository(self.session)
        student = await student_repo.get_by_id(student_id)

        if group and student:
            if student not in group.students:
                group.students.append(student)
                await self.session.commit()
            return True
        return False

    async def remove_student_from_group(self, student_id: int, group_id: int) -> bool:
        """
        Удалить студента из группы

        Args:
            student_id: ID студента
            group_id: ID группы

        Returns:
            True если удалён, False если студент не найден в группе
        """
        group = await self.get_by_id(group_id)
        student_repo = StudentRepository(self.session)
        student = await student_repo.get_by_id(student_id)

        if group and student and student in group.students:
            group.students.remove(student)
            await self.session.commit()
            return True
        return False