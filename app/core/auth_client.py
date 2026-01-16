
import httpx
from fastapi import HTTPException, status
from app.core.config import settings

async def validate_token(token: str) -> dict:
    async with httpx.AsyncClient(timeout=5) as client:
        res = await client.get(
            f"{settings.AUTH_SERVICE_URL}/auth/validate",
            headers={"Authorization": f"Bearer {token}"}
        )

    if res.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return res.json()
