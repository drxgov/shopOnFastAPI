from app.models import User
from sqlalchemy.orm import Session
from passlib.hash import argon2
from fastapi import HTTPException

def authUser(email: str,password: str,db:Session):
    dbuser = db.query(User).filter(User.email == email).first()
    if not dbuser:
        raise HTTPException(status_code=400, detail="Такой пользователь не существует")
    if not argon2.verify(password,dbuser.password):
        raise HTTPException(status_code=400, detail="неправильно введен пароль")
    return dbuser