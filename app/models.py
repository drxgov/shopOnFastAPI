from sqlalchemy import Integer,Column,String,Date,ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key = True,index = True)
    fullname = Column(String,nullable = False,index = True)
    password = Column(String,nullable = False)
    email = Column(String,nullable = False,unique = True)
    phoneNumber = Column(String,nullable = False,unique = True)
    birthdate = Column(Date,nullable = False)
    orders = relationship('Order',back_populates = 'ordering')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer,primary_key = True, index = True)
    dateOfOrder = Column(Date,nullable = False)
    nameOfItem = Column(String,nullable = False)
    userOrderID = Column(Integer,ForeignKey('users.id'))
    ordering = relationship('User',back_populates = 'orders')

