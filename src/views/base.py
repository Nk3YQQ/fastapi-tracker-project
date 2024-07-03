from pydantic import BaseModel

from src.crud import CRUD
from src.session import SessionManager


class View:
    """ Базовый класс для контроллеров """
    model = None

    def __init__(self, db):
        self._session = SessionManager(db)
        self.crud = CRUD(self._session, self.model)

    async def create(self, requested_data: BaseModel):
        pass

    async def read_all(self, skip: int = 0, limit: int = 10):
        pass

    async def read_one(self, instance_id: int):
        pass

    async def put(self, instance_id: int, requested_data: BaseModel):
        pass

    async def patch(self, instance_id: int, requested_data: BaseModel):
        pass

    async def delete(self, instance_id: int):
        pass
