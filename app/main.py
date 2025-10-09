from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import shop
from app.routes import profile
from app.routes import users
from app.database import Base,engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount('/static',StaticFiles(directory='static'),name = 'static')
templates = Jinja2Templates(directory = 'templates')

app.include_router(shop.router)
app.include_router(users.router)
app.include_router(profile.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app',reload = True)