from app.models import User
from sqlalchemy.orm import Session
from app.schemas import UserCreate
from app.models import User
from passlib.hash import argon2



def registerUser(tempuser: UserCreate, db: Session):
    finduser = db.query(User).filter(User.email == tempuser.email).first()
    if finduser: raise ValueError("Пользователь с таким email уже существует")
    print(f'hash pass {argon2.hash(tempuser.password)}')
    newuser = User(
        fullname = tempuser.fullname,
        email = tempuser.email,
        password = argon2.hash(tempuser.password),
        phoneNumber = tempuser.phoneNumber,
        birthdate = tempuser.birthdate
    )
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser