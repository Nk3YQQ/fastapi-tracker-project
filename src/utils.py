import json

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine


def create_asyncpg_engine(postgres_schema, params: dict):
    """ Функция создаёт асинхронное подключение """
    data = postgres_schema(
        driver=params.get('driver'),
        user=params.get('user'),
        password=params.get('password'),
        host=params.get('host'),
        db_name=params.get('db_name'),
    )

    url = f"postgresql+{data.driver}://{data.user}:{data.password}@{data.host}:5432/{data.db_name}"

    return create_async_engine(url)


def generate_new_id(instance, instance_list):
    """ Генерация нового id для сущности """
    if isinstance(instance.id, int):
        instance.id = len(instance_list) + 1


def check_object_or_400(instance, instance_list, model):
    """ Проверка объекта или возвращение ошибки 400 """
    if instance in instance_list:
        raise HTTPException(status_code=400, detail=f'{model.__class__.__name__} is already registered')
    return instance


def get_object_or_404(instance, model):
    """ Проверка объекта или возвращение ошибки 404 """
    if not instance:
        raise HTTPException(status_code=404, detail=f'{model.__class__} not found')
    return instance


def open_json_file(filepath):
    """ Чтение json файла и преобразование в список словарей """
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)
