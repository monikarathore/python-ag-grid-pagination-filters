from typing import Optional
from fastapi import Header, HTTPException
from app.core.config import settings
def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split(" ")[1]
    if token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid token")
