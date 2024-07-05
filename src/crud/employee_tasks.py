from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Employee, Task
from src.session import SessionTwoObjectManager


class EmployeeTaskCRUD:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.session = SessionTwoObjectManager(db, Employee, Task)

    async def get_employees_tasks(self):
        return await self.session.get_employees_tasks()

    async def get_potential_employing_task(self):
        return await self.session.get_potential_employing_task()
