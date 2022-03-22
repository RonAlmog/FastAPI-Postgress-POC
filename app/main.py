from typing import Optional
from urllib.request import Request
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import schemas, models, utils
from typing import List
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapidb', user='postgres', password='456456',
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error is:', error)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Worldz"}
