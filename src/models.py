from datetime import date
import enum

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from typing_extensions import Annotated

intpk = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True)]

email_field = Annotated[str, mapped_column(unique=True, nullable=False)]

birth_date = Annotated[date, mapped_column(Date, nullable=False)]

str_50 = Annotated[str, mapped_column(String(50), nullable=False)]
str_100 = Annotated[str, mapped_column(String(100), nullable=False)]

employee_id = Annotated[int, mapped_column(ForeignKey("employees.id"))]


class Base(DeclarativeBase):
    """ Базовый класс для моделей """
    pass


class Employee(Base):
    """ Модель сотрудника """
    __tablename__ = 'employees'

    id: Mapped[intpk]
    first_name: Mapped[str_100]
    last_name: Mapped[str_100]
    email: Mapped[email_field]
    title: Mapped[str_50]
    birth_date: Mapped[birth_date]

    tasks = relationship("Task", back_populates="employee", cascade="all, delete-orphan")


class Status(enum.Enum):
    """ Статусы задачи """
    pending = "pending"
    received = "received"
    completed = "completed"


class Task(Base):
    """ Модель для задачи """
    __tablename__ = 'tasks'

    id: Mapped[intpk]
    title: Mapped[str_50]
    status: Mapped[Status]
    employee_id: Mapped[employee_id]

    employee = relationship("Employee", back_populates="tasks")
