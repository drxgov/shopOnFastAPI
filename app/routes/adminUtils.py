from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get('/additem')
async def addItem(request: Request):
    userlogin = request.cookies.get('user_login')
    return templates.TemplateResponse('addItem.html',{
        'request':request,
        'userlogin':userlogin
    })

@router.get('/admin')
async def getAdminPanel(request: Request):
    return templates.TemplateResponse('adminPanel.html')