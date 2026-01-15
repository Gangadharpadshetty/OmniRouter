from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService
from app.utils.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(
    req: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        user = await service.register(req.email, req.password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    req: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        return await service.login(req.email, req.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService
from app.utils.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(
    req: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        user = await service.register(req.email, req.password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(
    req: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        return await service.login(req.email, req.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
