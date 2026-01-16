from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router

app = FastAPI(title="Auth Service")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://omnirouter-j94q.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
