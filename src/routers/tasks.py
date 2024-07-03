from fastapi import status, Depends

from src.routers.base import APIRouter
from src.schemas import Task, TaskCreate, TaskPut, TaskPatch
from src.views.tasks import TaskView

router = APIRouter()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(response_data: TaskCreate, view: TaskView = Depends()):
    created_task = await view.create(response_data)

    return created_task


@router.get("/", response_model=list[Task])
async def read_tasks(view: TaskView = Depends(), skip: int = 0, limit: int = 10):
    tasks_list = await view.read_all(skip, limit)

    return tasks_list


@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int, view: TaskView = Depends()):
    task = await view.read_one(task_id)

    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, response_data: TaskPut, view: TaskView = Depends()):
    task = await view.put(task_id, response_data)

    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task_particular(task_id: int, response_data: TaskPatch, view: TaskView = Depends()):
    task = await view.patch(task_id, response_data)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, view: TaskView = Depends()):
    await view.delete(task_id)
