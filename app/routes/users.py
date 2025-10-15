from fastapi import APIRouter,Request,HTTPException,Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.service import register
from app.service import auth
from app.service import utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/logout")
async def logoutUser():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie('user_login')
    return response

@router.get('/login')
async def getLoginPage(request: Request):
    return templates.TemplateResponse('login.html',{'request':request})

@router.post('/login')
async def loginUser(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    dbuser = auth.authUser(email,password,db)
    if not dbuser: return templates.TemplateResponse('login.html',{
        "request":request,
        "error":"неверный логин или пароль"
    })
    response = RedirectResponse(url = '/profile',status_code = 303)
    access_token = utils.create_access_token(data={"sub": dbuser.email})
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,        
        max_age=60*60*24*7,
        samesite="lax"
    )
    response.set_cookie(
        key="user_login",
        value = True
    )
    return response

@router.get('/register')
async def getRegisterPage(request: Request):
    return templates.TemplateResponse('register.html',{'request':request})

@router.post('/register')
async def registerUser(
    request: Request,
    fullname: str = Form(...),
    email: str = Form(...),
    phoneNumber: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    birthdate: str = Form(...),
    db: Session = Depends(get_db)
):
    from app.schemas import UserCreate
    from datetime import datetime

    if password != confirm_password:
        return templates.TemplateResponse('register.html',{
            'request':request,
            'error':"пароли не совпадают"
            })

    try:
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
    except ValueError:
        return templates.TemplateResponse('register.html',{
            'request':request,
            'error':"дата рождения не корректна"
            })

    try:
        user = UserCreate(
            fullname=fullname,
            email=email,
            phoneNumber=phoneNumber,
            password=password,
            birthdate=birthdate_obj
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    user = register.registerUser(user, db=db)
    if not user:
        return templates.TemplateResponse('register.html',{
            'request':request,
            'error':"пользователь с таким мылом уже существует"
            })

    return RedirectResponse(url="/login", status_code=303)
