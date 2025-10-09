from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.service import utils

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/profile")
async def profile(request: Request, db: Session = Depends(get_db)):
    xuser = request.cookies.get("access_token")
    if not xuser: return RedirectResponse('/login',status_code = 303)
    xuser = utils.get_current_user_from_request(request,db)
    if not xuser: return RedirectResponse('/login',status_code = 303)
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": xuser,
        "userlogin":True,
        })