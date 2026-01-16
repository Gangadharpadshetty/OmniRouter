from jose import jwt, JWTError
from app.core.config import settings

def verify_token(token: str) -> str | None:
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload.get("sub")
    except JWTError:
        return None
