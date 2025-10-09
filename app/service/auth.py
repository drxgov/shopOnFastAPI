from app.models import User
from sqlalchemy.orm import Session
from passlib.hash import argon2

def authUser(email: str,password: str,db:Session):
    dbuser = db.query(User).filter(User.email == email).first()
    if not dbuser: return None
    if not argon2.verify(password,dbuser.password):return None 
    return dbuser