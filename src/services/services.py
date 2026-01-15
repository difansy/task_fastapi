"""
Service Layer - бизнес-логика приложения
Обрабатывает запросы от API, проверяет условия, вызывает репозитории
"""
from src.repositories.repositories import StudentRepository, GroupRepository
from src.schemas.schemas import StudentCreate, GroupCreate


class StudentService:
    """Сервис для работы со студентами"""

    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def create_student(self, student_data: StudentCreate):
        """
        Создать нового студента

        Args:
            student_data: Данные для создания студента

        Returns:
            Созданный студент
        """
        return await self.repository.create(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            email=student_data.email
        )

    async def get_student(self, student_id: int):
        """
        Получить студента по ID

        Args:
            student_id: ID студента

        Returns:
            Студент

        Raises:
            ValueError: Если студент не найден
        """
        student = await self.repository.get_by_id(student_id)
        if not student:
            raise ValueError(f"Студент с ID {student_id} не найден")
        return student

    async def get_all_students(self):
        """
        Получить всех студентов

        Returns:
            Список студентов
        """
        return await self.repository.get_all()

    async def delete_student(self, student_id: int):
        """
        Удалить студента по ID

        Args:
            student_id: ID студента

        Returns:
            Сообщение об успехе

        Raises:
            ValueError: Если студент не найден
        """
        success = await self.repository.delete(student_id)
        if not success:
            raise ValueError(f"Студент с ID {student_id} не найден")
        return {"message": "Студент успешно удален"}


class GroupService:
    """Сервис для работы с группами"""

    def __init__(self, repository: GroupRepository):
        self.repository = repository

    async def create_group(self, group_data: GroupCreate):
        """
        Создать новую группу

        Args:
            group_data: Данные для создания группы

        Returns:
            Созданная группа
        """
        return await self.repository.create(
            name=group_data.name,
            description=group_data.description
        )

    async def get_group(self, group_id: int):
        """
        Получить группу по ID

        Args:
            group_id: ID группы

        Returns:
            Группа

        Raises:
            ValueError: Если группа не найдена
        """
        group = await self.repository.get_by_id(group_id)
        if not group:
            raise ValueError(f"Группа с ID {group_id} не найдена")
        return group

    async def get_all_groups(self):
        """
        Получить все группы

        Returns:
            Список групп
        """
        return await self.repository.get_all()

    async def delete_group(self, group_id: int):
        """
        Удалить группу по ID

        Args:
            group_id: ID группы

        Returns:
            Сообщение об успехе

        Raises:
            ValueError: Если группа не найдена
        """
        success = await self.repository.delete(group_id)
        if not success:
            raise ValueError(f"Группа с ID {group_id} не найдена")
        return {"message": "Группа успешно удалена"}

    async def add_student_to_group(self, student_id: int, group_id: int):
        """
        Добавить студента в группу

        Args:
            student_id: ID студента
            group_id: ID группы

        Returns:
            Сообщение об успехе

        Raises:
            ValueError: Если студент или группа не найдены
        """
        success = await self.repository.add_student_to_group(student_id, group_id)
        if not success:
            raise ValueError("Студент или группа не найдены")
        return {"message": f"Студент {student_id} добавлен в группу {group_id}"}

    async def remove_student_from_group(self, student_id: int, group_id: int):
        """
        Удалить студента из группы

        Args:
            student_id: ID студента
            group_id: ID группы

        Returns:
            Сообщение об успехе

        Raises:
            ValueError: Если студент не найден в группе
        """
        success = await self.repository.remove_student_from_group(student_id, group_id)
        if not success:
            raise ValueError("Студент не найден в этой группе")
        return {"message": f"Студент {student_id} удален из группы {group_id}"}

    async def transfer_student(self, student_id: int, from_group_id: int, to_group_id: int):
        """
        Перевести студента из одной группы в другую

        Args:
            student_id: ID студента
            from_group_id: ID исходной группы
            to_group_id: ID целевой группы

        Returns:
            Сообщение об успехе

        Raises:
            ValueError: Если операция не удалась
        """
        # Удаляем из старой группы
        await self.repository.remove_student_from_group(student_id, from_group_id)

        # Добавляем в новую группу
        success = await self.repository.add_student_to_group(student_id, to_group_id)
        if not success:
            raise ValueError("Ошибка при переводе студента")

        return {
            "message": f"Студент {student_id} переведен из группы {from_group_id} в группу {to_group_id}"
        }