"""
ORM модели для базы данных.
Описывают структуру таблиц Student, Group и их связи
"""
from sqlalchemy import String, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base

# Эта таблица связывает студентов и группы
# Один студент может быть в нескольких группах
# Одна группа может содержать нескольких студентов
student_group_association = Table(
    "student_group_association",  # Имя таблицы в БД
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)
)


class Student(Base):
    """
    Модель студента
    Таблица: students
    """
    __tablename__ = "students"

    # Первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Имя студента (обязательное поле, макс 100 символов)
    first_name: Mapped[str] = mapped_column(String(100))

    # Фамилия студента (обязательное поле, макс 100 символов)
    last_name: Mapped[str] = mapped_column(String(100))

    # Email студента (обязательное, уникальное поле, макс 200 символов)
    email: Mapped[str] = mapped_column(String(200), unique=True)

    # Связь многие-ко-многим с группами
    # back_populates - создаёт двустороннюю связь
    groups: Mapped[list["Group"]] = relationship(
        secondary=student_group_association,  # Через промежуточную таблицу
        back_populates="students"  # Обратная связь в модели Group
    )

    def __repr__(self):
        """Строковое представление объекта"""
        return f"<Student(id={self.id}, name={self.first_name} {self.last_name})>"


class Group(Base):
    """
    Модель группы студентов
    Таблица: groups
    """
    __tablename__ = "groups"

    # Первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Название группы (обязательное, уникальное поле, макс 100 символов)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Описание группы (необязательное поле, макс 500 символов)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Связь многие-ко-многим со студентами
    students: Mapped[list["Student"]] = relationship(
        secondary=student_group_association,
        back_populates="groups"
    )

    def __repr__(self):
        """Строковое представление объекта"""
        return f"<Group(id={self.id}, name={self.name})>"