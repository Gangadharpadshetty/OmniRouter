from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes.projects import router as projects_router
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Project Service")

origins = [
    "https://omnirouter-j94q.onrender.com",  # production frontend
    "http://localhost:3000",                 # local dev
    "http://localhost:5173",                 # Vite dev
    "http://127.0.0.1:3000",                 # alternative localhost
    "http://127.0.0.1:5173",                 # alternative localhost for Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # ❌ do NOT use ["*"] with credentials
    allow_credentials=True,
    allow_methods=["*"],            # allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],            # allows Content-Type, Authorization, etc.
    expose_headers=["*"],           # optional but helpful
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


@app.get("/")
async def root():
    return {"service": "Project Service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(projects_router)
