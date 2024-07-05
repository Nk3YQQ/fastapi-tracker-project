from fastapi import status, Depends, APIRouter

from src.crud.employees import EmployeeCRUD
from src.schemas import Employee, EmployeeCreate, EmployeePut, EmployeePatch

router = APIRouter()


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(response_data: EmployeeCreate, crud: EmployeeCRUD = Depends()):
    created_employee = await crud.create_instance(response_data)

    return created_employee


@router.get("/", response_model=list[Employee])
async def read_employees(crud: EmployeeCRUD = Depends(), skip: int = 0, limit: int = 10):
    employees_list = await crud.read_all_instances(skip, limit)

    return employees_list


@router.get("/{employee_id}", response_model=Employee)
async def read_employee(employee_id: int, crud: EmployeeCRUD = Depends()):
    employee = await crud.read_one_instance(employee_id)

    return employee


@router.put("/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, response_data: EmployeePut, crud: EmployeeCRUD = Depends()):
    employee = await crud.update_instance(employee_id, response_data)

    return employee


@router.patch("/{employee_id}", response_model=Employee)
async def update_employee_particular(employee_id: int, response_data: EmployeePatch, crud: EmployeeCRUD = Depends()):

    employee = await crud.update_instance(employee_id, response_data)

    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, crud: EmployeeCRUD = Depends()):
    await crud.delete_instance(employee_id)
