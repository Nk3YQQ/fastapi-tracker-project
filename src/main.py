from fastapi import FastAPI

from src.routers.employees import router as employees_router
from src.routers.tasks import router as tasks_router
from src.routers.employees_tasks import router as employees_tasks_router

app = FastAPI(title='Tracker App')


app.include_router(employees_router, prefix='/employees', tags=['employees'])
app.include_router(tasks_router, prefix='/tasks', tags=['tasks'])
app.include_router(employees_tasks_router, prefix='/employees/tasks', tags=['employees_tasks'])
