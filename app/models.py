from sqlalchemy import Integer,Column,String,Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key = True,index = True)
    fullname = Column(String,nullable = False,index = True)
    password = Column(String,nullable = False)
    email = Column(String,nullable = False,unique = True)
    phoneNumber = Column(String,nullable = False,unique = True)
    birthdate = Column(Date,nullable = False)