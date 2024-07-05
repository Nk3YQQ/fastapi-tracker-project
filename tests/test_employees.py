import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio(scope='module')
async def test_create_employee(async_client: AsyncClient, employee_list: list[dict]) -> None:
    """ Тестирование создание сотрудников """
    for employee_data in employee_list:
        response = await async_client.post("/employees/", json=employee_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio(scope='module')
async def test_read_all_employees(async_client: AsyncClient) -> None:
    """ Тестирование чтения всех сотрудников """
    response = await async_client.get("/employees/")
    assert response.status_code == status.HTTP_200_OK

    content = response.json()

    assert len(content) == 5


@pytest.mark.asyncio(scope='module')
async def test_read_one_employee(async_client: AsyncClient) -> None:
    """ Тестирование чтения одного сотрудника """
    employee_id = 2

    response = await async_client.get(f"/employees/{employee_id}")
    assert response.status_code == status.HTTP_200_OK

    content = response.json()

    assert content.get('first_name') == "Ivan"
    assert content.get('last_name') == "Ivanov"
    assert content.get('email') == "ivan.ivanov@mail.ru"
    assert content.get('title') == "Senior Python-developer"
    assert content.get('birth_date') == "1993-04-09"


@pytest.mark.asyncio(scope='module')
async def test_delete_employee(async_client: AsyncClient) -> None:
    """ Тестирование удаления сотрудника """
    employee_id = 3

    response = await async_client.delete(f"/employees/{employee_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
