from fastapi import Header, HTTPException

def get_bearer_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    return authorization.split(" ")[1]
