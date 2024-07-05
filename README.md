# Результаты тестирования
![Workflow Status](https://github.com/Nk3YQQ/fastapi-tracker-project/actions/workflows/main.yml/badge.svg)


# Описание проекта

fastapi-tracker-project - API для трекера задач сотрудников. 

Основной стек проекта:
```
fastapi[all]
sqlalchemy[asyncio]
asyncpg
alembic
databases
python-dotenv
flake8
typing_extensions # Входит в fastapi[all]
pydantic # Входит в fastapi[all]
pytest
pytest-asyncio
httpx # Входит в fastapi[all]
```

В приложении реализован асинхронный подход, то есть основные компоненты работают асинхронно (база данных, сессия, crud и эндпоинты).

# Как пользоваться проектом

## 1) Скопируйте проект на Ваш компьютер
```
git clone git@github.com:Nk3YQQ/drf-tracker-project.git
```

## 2) Добавьте файл .env для переменных окружения
Чтобы запустить проект, понадобятся переменные окружения, которые необходимо добавить в созданный Вами .env файл.

Пример переменных окружения необходимо взять из файла .env.sample

## 3) Запустите проект
Запуск проекта
```
make run
```

Остановка проекта
```
make stop
```

P.S. Убедитесь, что на Вашей локальной машине установлены docker и docker-compose, потому что без них не получится запустить проект.
