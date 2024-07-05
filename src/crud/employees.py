from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.database import get_db
from src.models import Employee


class EmployeeCRUD(CRUD):
    model = Employee

    def __init__(self, db: AsyncSession = Depends(get_db)):
        super().__init__(db)
