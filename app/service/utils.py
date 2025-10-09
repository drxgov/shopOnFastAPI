from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models

SECRET_KEY = 'super_mega_secret_key'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_from_request(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token: return RedirectResponse(url='/login', status_code=303)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None: return RedirectResponse(url='/login', status_code=303)
    except JWTError:
        return RedirectResponse(url='/login', status_code=303)

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None: return RedirectResponse(url='/login', status_code=303)

    return user
