from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SessionManager:
    """ Класс для работы с базой данных """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, instance):
        """ Создание объекта """
        try:
            self.db.add(instance)
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f'Ошибка в добавлении сущности: {e}')
        finally:
            await self.db.commit()
            await self.db.refresh(instance)

    async def all(self, model, skip: int = 0, limit: int = 10):
        """ Чтение всех объектов """
        try:
            result = await self.db.execute(select(model).offset(skip).limit(limit))
            return result.scalars().all()
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f'Ошибка в чтение всех сущностей: {e}')

    async def get(self, model, instance_id: int):
        """ Чтение одного объекта """
        try:
            result = await self.db.execute(select(model).filter(model.id == instance_id))
            return result.scalars().first()
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f'Ошибка в чтении сущности: {e}')

    async def update(self, model, instance_id: int, data: dict):
        """ Обновление объекта """
        try:
            instance = await self.db.get(model, instance_id)

            for key, value in data.items():
                if hasattr(instance, key) and value:
                    setattr(instance, key, value)

            self.db.add(instance)

            return instance

        except Exception as e:
            await self.db.rollback()
            raise ValueError(f'Ошибка в обновлении сущности: {e}')

        finally:
            await self.db.commit()

    async def delete(self, model, instance_id: int):
        """ Удаление объекта """
        try:
            instance = await self.db.get(model, instance_id)
            await self.db.delete(instance)
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f'Ошибка в удалении сущности: {e}')
        finally:
            await self.db.commit()
