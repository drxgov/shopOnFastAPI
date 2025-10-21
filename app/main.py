from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import shop
from app.routes import profile
from app.routes import users
from app.routes import adminUtils
from app.database import engine
from app.models import User,Item,Category,Order
from sqladmin import Admin, ModelView

app = FastAPI()
admin = Admin(app, engine)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.fullname, User.email,User.phoneNumber,User.adminStatus]

class ItemAdmin(ModelView,model = Item):
    column_list = [Item.id,Item.itemName,Item.itemDescription,Item.itemAvilable,Item.itemCount,Item.category]

admin.add_view(UserAdmin)
admin.add_view(ItemAdmin)

app.mount('/static',StaticFiles(directory='static'),name = 'static')
templates = Jinja2Templates(directory = 'templates')

app.include_router(shop.router)
app.include_router(users.router)
app.include_router(profile.router)
app.include_router(adminUtils.router)