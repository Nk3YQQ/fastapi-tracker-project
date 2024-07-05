from sqlalchemy import select, func, or_, and_, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import Status


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


class SessionTwoObjectManager:
    """ В отличие от класса выше, данный отвечает
    за работу с двумя сущностями одновременно """

    def __init__(self, db: AsyncSession, employee_model, task_model):
        self.db = db
        self.employee = employee_model
        self.task = task_model

    async def get_employees_tasks(self):
        status_filter_condition = or_(self.task.id.is_(None), self.task.status.in_([Status.received, Status.pending]))

        statement = (
            select(self.employee)
            .options(joinedload(self.employee.tasks))
            .outerjoin(self.employee.tasks)
            .filter(status_filter_condition)
            .group_by(self.employee.id)
            .order_by(func.count(self.task.id).desc())
        )

        results = await self.db.execute(statement)

        return results.unique().scalars().all()

    async def get_important_tasks(self):
        subquery = (
            select(self.task.parent_task_id)
            .where(self.task.status.in_(["pending", "received"]))
            .distinct()
            .subquery()
        )

        statement = (
            select(self.task)
            .where(
                and_(
                    self.task.employee_id.is_(None),
                    self.task.id.in_(subquery)
                )
            )
            .distinct()
        )

        results = await self.db.execute(statement)

        return results.unique().scalars().all()

    async def get_less_working_employee(self):
        tasks_counts_subquery = (
            select(self.task.employee_id.label('employee_id'), func.count(self.task.id).label('task_count'))
            .group_by(self.task.employee_id)
            .cte('tasks_counts')
        )

        min_tasks_count_subquery = (
            select(func.min(tasks_counts_subquery.c.task_count).label('min_task_count'))
            .cte('min_task_count')
        )

        statement = (
            select(self.employee)
            .join(tasks_counts_subquery, self.employee.id == tasks_counts_subquery.c.employee_id)
            .join(min_tasks_count_subquery, literal(True))
            .where(
                or_(
                    tasks_counts_subquery.c.task_count == min_tasks_count_subquery.c.min_task_count,
                    and_(
                        tasks_counts_subquery.c.task_count <= min_tasks_count_subquery.c.min_task_count + 2,
                        select(1)
                        .where(self.task.employee_id == self.employee.id)
                        .where(self.task.parent_task_id.isnot(None))
                        .exists()
                    )
                )
            )
        )

        results = await self.db.execute(statement)

        return results.unique().scalars().all()

    async def get_potential_employing_task(self):
        important_tasks = await self.get_important_tasks()

        less_working_employees = await self.get_less_working_employee()

        converted_less_working_employees = list(
            map(lambda x: f"{x.first_name} {x.last_name}", less_working_employees)
        )

        list_of_important_tasks_with_employees = []

        for important_task in important_tasks:
            title = important_task.title
            deadline = important_task.deadline

            converted_important_task = {
                'title': title,
                'deadline': deadline,
                'employees': converted_less_working_employees
            }

            list_of_important_tasks_with_employees.append(converted_important_task)

        return list_of_important_tasks_with_employees
