runserver:
	uvicorn src.main:app --reload

migrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

test:
	pytest tests/test_employees.py
	pytest tests/test_tasks.py
