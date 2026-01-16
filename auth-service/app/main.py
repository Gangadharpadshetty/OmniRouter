from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router

app = FastAPI(title="Auth Service")

# ✅ Explicit allowed origins
origins = [
    "https://omnirouter-j94q.onrender.com",  # production frontend
    "http://localhost:3000",                 # local dev (optional)
    "http://localhost:5173",                 # Vite dev (optional)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # ❌ do NOT use ["*"] with credentials
    allow_credentials=True,
    allow_methods=["*"],            # allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],            # allows Content-Type, Authorization, etc.
    expose_headers=["*"],           # optional but helpful
)

app.include_router(auth_router)
