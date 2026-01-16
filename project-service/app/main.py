from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.projects import router as projects_router

app = FastAPI(title="Project Service")

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


@app.get("/")
async def root():
    return {"service": "Project Service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(projects_router)
