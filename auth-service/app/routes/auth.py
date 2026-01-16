from fastapi import APIRouter, Depends, HTTPException, Header
from app.schemas.user import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService
from app.utils.dependencies import get_auth_service
from app.core.security import verify_token

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


@router.get("/validate")
async def validate_token(authorization: str = Header(None)):
    """Validate JWT token and return user_id. Used by other services for authentication."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    # Verify token
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {"user_id": user_id, "valid": True}
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
