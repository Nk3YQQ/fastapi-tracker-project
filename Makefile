runserver:
	alembic upgrade head
	uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

test:
	pytest tests/test_employees.py
	pytest tests/test_tasks.py
	pytest tests/test_employees_tasks.py

container-tests:
	docker-compose up --build -d
	docker-compose exec -T app make test
	docker-compose exec -T app flake8 src/
	docker-compose exec -T app flake8 tests/
	docker-compose down --volumes

run:
	docker-compose up --build -d

stop:
	docker-compose down --volumes
