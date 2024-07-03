from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Task
from src.views.base import View


class TaskView(View):
    """ Контроллер для задач """
    model = Task

    def __init__(self, db: AsyncSession = Depends(get_db)):
        super().__init__(db)

    async def create(self, requested_data: BaseModel):
        return await self.crud.create_instance(requested_data)

    async def read_all(self, skip: int = 0, limit: int = 10):
        return await self.crud.read_all_instances(skip, limit)

    async def read_one(self, instance_id: int):
        return await self.crud.read_one_instance(instance_id)

    async def put(self, instance_id: int, requested_data: BaseModel):
        return await self.crud.update_instance(instance_id, requested_data)

    async def patch(self, instance_id: int, requested_data: BaseModel):
        return await self.crud.update_instance(instance_id, requested_data)

    async def delete(self, instance_id: int):
        return await self.crud.delete_instance(instance_id)
