from urllib.request import Request
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from .database import engine
from . import models
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Worldz"}
