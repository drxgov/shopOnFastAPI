from fastapi import APIRouter,Request,HTTPException,Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.service import register
from passlib.hash import argon2
from app.service import auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/profile")
async def profile(request: Request, db: Session = Depends(get_db)):
    from app.models import User
    xuser = request.cookies.get("user_email")
    if not xuser: return RedirectResponse('/login',status_code = 303)
    dbuser = db.query(User).filter(User.email == xuser).first()
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": dbuser,
        "userlogin":True,
        })


@router.get('/login')
async def getLoginPage(request: Request):
    return templates.TemplateResponse('login.html',{'request':request})

@router.post('/login')
async def loginUser(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    dbuser = auth.authUser(email,password,db)
    response = RedirectResponse(url = '/profile',status_code = 303)
    response.set_cookie(
        key="user_email", 
        value=dbuser.email, 
        httponly=True,        # чтобы не достать из JS
        max_age=60*60*24*7,   # неделя
        samesite="lax"
    )
    return response

@router.get('/register')
async def getRegisterPage(request: Request):
    return templates.TemplateResponse('register.html',{'request':request})

@router.post('/register')
async def registerUser(
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
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    try:
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректная дата рождения")

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

    try: 
        register.registerUser(user, db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url="/login", status_code=303)
