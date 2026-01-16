from fastapi import Depends
from app.utils.security import get_bearer_token
from app.core.auth_client import validate_token

async def get_current_user(token: str = Depends(get_bearer_token)):
    return await validate_token(token)
