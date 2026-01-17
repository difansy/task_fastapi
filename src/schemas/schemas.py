"""
Pydantic схемы для валидации входных и выходных данных
Используются в API эндпоинтах для проверки данных
"""
from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    """Базовая схема студента с общими полями"""
    first_name: str
    last_name: str
    email: EmailStr


class StudentCreate(StudentBase):
    """
    Схема для создания студента
    Используется в POST /students
    """
    pass


class StudentResponse(StudentBase):
    """
    Схема для ответа API с данными студента
    Используется в GET /students/{id}
    """
    id: int

    # Настройка для работы с ORM моделями
    model_config = ConfigDict(from_attributes=True)


class StudentWithGroups(StudentResponse):
    """
    Схема студента со списком его групп
    Используется в GET /students/{id} для полной информации
    """
    groups: list["GroupResponse"] = []


class GroupBase(BaseModel):
    """Базовая схема группы с общими полями"""
    name: str
    description: str | None = None


class GroupCreate(GroupBase):
    """
    Схема для создания группы
    Используется в POST /groups
    """
    pass


class GroupResponse(GroupBase):
    """
    Схема для ответа API с данными группы
    Используется в GET /groups/{id}
    """
    id: int

    model_config = ConfigDict(from_attributes=True)


class GroupWithStudents(GroupResponse):
    """
    Схема группы со списком студентов
    Используется в GET /groups/{id} для полной информации
    """
    students: list[StudentResponse] = []


class AddStudentToGroup(BaseModel):
    """
    Схема для добавления студента в группу
    Используется в POST /groups/add-student
    """
    student_id: int
    group_id: int


class TransferStudent(BaseModel):
    """
    Схема для перевода студента между группами
    Используется в POST /groups/transfer-student
    """
    student_id: int
    from_group_id: int
    to_group_id: int