from fastapi import APIRouter, Depends

from src.crud.employee_tasks import EmployeeTaskCRUD
from src.schemas import EmployeesTasks, ImportantTask

router = APIRouter()


@router.get("/", response_model=list[EmployeesTasks])
async def get_employees_tasks(crud: EmployeeTaskCRUD = Depends(EmployeeTaskCRUD)):
    employees_tasks = await crud.get_employees_tasks()

    return employees_tasks


@router.get("/important_tasks", response_model=list[ImportantTask])
async def get_potential_employing_task(crud: EmployeeTaskCRUD = Depends(EmployeeTaskCRUD)):
    tasks = await crud.get_potential_employing_task()

    return tasks
