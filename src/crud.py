from pydantic import BaseModel

from src.utils import check_object_or_400, generate_new_id


class CRUD:
    """ Класс для CRUD-операций """

    def __init__(self, session, model):
        self.model = model
        self.session = session

    async def create_instance(self, requested_data: BaseModel):
        data = requested_data.model_dump()

        new_instance = self.model(**data)
        instance_list = await self.read_all_instances()

        generate_new_id(new_instance, instance_list)

        instance = check_object_or_400(new_instance, instance_list, self.model)
        await self.session.create(instance)

        return instance

    async def read_all_instances(self, skip: int = 0, limit: int = 10):
        instance_list = await self.session.all(self.model, skip, limit)

        return instance_list

    async def read_one_instance(self, instance_id: int):
        instance = await self.session.get(self.model, instance_id)

        return instance

    async def update_instance(self, instance_id: int, requested_data: BaseModel):
        data = requested_data.model_dump()

        updated_instance = await self.session.update(self.model, instance_id, data)

        return updated_instance

    async def delete_instance(self, instance_id: int):
        await self.session.delete(self.model, instance_id)
