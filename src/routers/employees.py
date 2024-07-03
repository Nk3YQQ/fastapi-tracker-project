from fastapi import status, Depends

from src.routers.base import APIRouter
from src.schemas import Employee, EmployeeCreate, EmployeePut, EmployeePatch
from src.views.employees import EmployeeView

router = APIRouter()


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(response_data: EmployeeCreate, view: EmployeeView = Depends()):
    created_employee = await view.create(response_data)

    return created_employee


@router.get("/", response_model=list[Employee])
async def read_employees(view: EmployeeView = Depends(), skip: int = 0, limit: int = 10):
    employees_list = await view.read_all(skip, limit)

    return employees_list


@router.get("/{employee_id}", response_model=Employee)
async def read_employee(employee_id: int, view: EmployeeView = Depends()):
    employee = await view.read_one(employee_id)

    return employee


@router.put("/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, response_data: EmployeePut, view: EmployeeView = Depends()):
    employee = await view.put(employee_id, response_data)

    return employee


@router.patch("/{employee_id}", response_model=Employee)
async def update_employee_particular(employee_id: int, response_data: EmployeePatch, view: EmployeeView = Depends()):
    employee = await view.patch(employee_id, response_data)

    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, view: EmployeeView = Depends()):
    await view.delete(employee_id)
