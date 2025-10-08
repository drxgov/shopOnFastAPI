from pydantic import BaseModel,EmailStr,constr,validator
from datetime import date

class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    phoneNumber: constr(min_length = 10, max_length = 15)
    password: constr(min_length = 6)
    birthdate: date

    @validator('fullname')
    def checkFullname(cls,v):
        if len(v.split()) < 2:
            raise ValueError("фио должно содержать минимум два слова")
        return v

    @validator('phoneNumber')
    def checkPhoneNumber(cls,v):
        if not v.replace("+", "").replace(" ", "").isdigit():
            raise ValueError("Телефон должен содержать только цифры")
        return v


class userRead(BaseModel):
    id: int
    fullname: str 
    email: EmailStr
    phone: str
    birthdate: date

    class Config:
        from_attributes = True
    
class userLogin(BaseModel):
    email: EmailStr
    password: str
