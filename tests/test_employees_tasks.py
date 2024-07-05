import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio(scope='module')
async def test_create_tasks_and_employees(
        async_client: AsyncClient,
        tasks_list: list[dict],
        employee_list: list[dict]) -> None:

    for employee_data in employee_list:
        await async_client.post("/employees/", json=employee_data)
    for task_data in tasks_list:
        response = await async_client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio(scope='module')
async def test_get_employees_tasks(async_client: AsyncClient) -> None:
    response = await async_client.get('/employees/tasks/')

    assert response.status_code == status.HTTP_200_OK

    employees = response.json()

    assert isinstance(employees, list)

    first_employee = employees[0]

    assert isinstance(first_employee, dict)

    first_name = first_employee['first_name']
    last_name = first_employee['last_name']
    title = first_employee['title']
    tasks = first_employee['tasks']

    assert first_name == 'Ivan'
    assert last_name == 'Ivanov'
    assert title == 'Senior Python-developer'

    assert isinstance(tasks, list)


@pytest.mark.asyncio(scope='module')
async def test_get_potential_employing_task(async_client: AsyncClient) -> None:
    response = await async_client.get('/employees/tasks/important_tasks')

    assert response.status_code == status.HTTP_200_OK

    tasks = response.json()

    assert isinstance(tasks, list)

    task = tasks[0]

    assert isinstance(task, dict)

    title = task['title']
    employees = task['employees']

    assert title == 'Make deploy'

    assert isinstance(employees, list)
