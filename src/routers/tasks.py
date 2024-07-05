from fastapi import status, Depends, APIRouter

from src.crud.tasks import TaskCRUD
from src.schemas import Task, TaskCreate, TaskPut, TaskPatch

router = APIRouter()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(response_data: TaskCreate, crud: TaskCRUD = Depends()):
    created_task = await crud.create_instance(response_data)

    return created_task


@router.get("/", response_model=list[Task])
async def read_tasks(crud: TaskCRUD = Depends(), skip: int = 0, limit: int = 10):
    tasks_list = await crud.read_all_instances(skip, limit)

    return tasks_list


@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int, crud: TaskCRUD = Depends()):
    task = await crud.read_one_instance(task_id)

    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, response_data: TaskPut, crud: TaskCRUD = Depends()):
    task = await crud.update_instance(task_id, response_data)

    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task_particular(task_id: int, response_data: TaskPatch, crud: TaskCRUD = Depends()):
    task = await crud.update_instance(task_id, response_data)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, crud: TaskCRUD = Depends()):
    await crud.delete_instance(task_id)
