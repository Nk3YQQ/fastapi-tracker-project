import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio(scope='module')
async def test_create_task(async_client: AsyncClient, tasks_list: list[dict], employee_list: list[dict]) -> None:
    for employee_data in employee_list:
        await async_client.post("/employees/", json=employee_data)
    for task_data in tasks_list:
        response = await async_client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio(scope='module')
async def test_read_all_task(async_client: AsyncClient) -> None:
    response = await async_client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK

    content = response.json()

    assert len(content) == 6

    pending_tasks = list(task for task in content if task['status'] == 'pending')

    assert len(pending_tasks) == 4


@pytest.mark.asyncio(scope='module')
async def test_read_one_task(async_client: AsyncClient) -> None:
    task_id = 3

    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK

    content = response.json()

    assert content.get('title') == "Create containers"
    assert content.get('status') == "pending"
    assert content.get('employee_id') == 2


@pytest.mark.asyncio(scope='module')
async def test_delete_task(async_client: AsyncClient) -> None:
    task_id = 3

    response = await async_client.delete(f"/tasks/{task_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
