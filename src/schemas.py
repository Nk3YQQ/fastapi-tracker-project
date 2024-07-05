from datetime import date
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

str_50 = Annotated[str, Field(max_length=50)]


class Status(str, Enum):
    """ Статусы задачи """
    pending = "pending"
    received = "received"
    completed = "completed"


status = Annotated[Status, Field(default="received")]


class TaskBaseModel(BaseModel):
    """ Базовая модель для задачи """
    title: str_50
    status: status
    deadline: date
    employee_id: int | None = None
    parent_task_id: int | None = None

    model_config = ConfigDict(use_enum_values=True)


class TaskCreate(TaskBaseModel):
    """ Модель для POST-запроса задачи """
    pass


class Task(TaskBaseModel):
    """ Модель для GET-запроса задачи """
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskPut(TaskBaseModel):
    """ Модель для PUT-запроса задачи """
    pass


class TaskPatch(BaseModel):
    """ Модель для PATCH-запроса задачи """
    title: str_50 | None = None
    status: Status | None = None
    deadline: date | None = None
    employee_id: int | None = None
    parent_task_id: int | None = None


class EmployeeBaseModel(BaseModel):
    """ Базовая модель для сотрудника"""
    first_name: str
    last_name: str
    email: str
    title: str
    birth_date: date


class EmployeeCreate(EmployeeBaseModel):
    """ Модель для POST-запроса сотрудника """
    pass


class Employee(EmployeeBaseModel):
    """ Модель для GET-запроса сотрудника """
    id: int

    model_config = ConfigDict(from_attributes=True)


class EmployeePut(EmployeeBaseModel):
    """ Модель для PUT-запроса сотрудника """
    pass


class EmployeePatch(BaseModel):
    """ Модель для PATCH-запроса сотрудника """
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    title: str | None = None
    birth_date: date | None = None


class EmployeesTasks(BaseModel):
    """ Модель для сотрудников и их задач """
    id: int
    first_name: str
    last_name: str
    email: str
    title: str
    birth_date: date
    tasks: list[Task] = []


class ImportantTask(BaseModel):
    """ Модель для важных задач """
    title: str
    deadline: date
    employees: list[str] = []
