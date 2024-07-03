from fastapi import FastAPI

from src.routers.employees import router as employees_router
from src.routers.tasks import router as tasks_router

app = FastAPI(title='Tracker App')


app.include_router(employees_router, prefix='/employees', tags=['employees'])
app.include_router(tasks_router, prefix='/tasks', tags=['tasks'])
