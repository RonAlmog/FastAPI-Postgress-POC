from typing import Optional
from urllib.request import Request
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import schemas
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


@app.get("/")
async def root():
    return {"message": "Hello Worldz"}


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createpost(post: schemas.Post, db: Session = Depends(get_db)):
    newpost = models.Post(**post.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)

    return {'data': newpost}


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return {'data': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):

    postquery = db.query(models.Post).filter(models.Post.id == id)
    post = postquery.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    postquery.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {'data': postquery.first()}
