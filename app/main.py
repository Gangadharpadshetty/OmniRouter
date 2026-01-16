from fastapi import FastAPI
from app.routes.projects import router as project_router

app = FastAPI(title="Project Service")

app.include_router(project_router)
