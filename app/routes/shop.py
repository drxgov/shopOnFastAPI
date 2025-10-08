from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get('/')
async def getMain(request: Request):
    userlogin = request.cookies.get("user_email")
    return templates.TemplateResponse('main.html',{
        'request':request,
        'userlogin':userlogin
        })