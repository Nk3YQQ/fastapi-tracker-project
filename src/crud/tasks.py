from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.database import get_db
from src.models import Task


class TaskCRUD(CRUD):
    """ CRUD для задач """
    model = Task

    def __init__(self, db: AsyncSession = Depends(get_db)):
        super().__init__(db)
