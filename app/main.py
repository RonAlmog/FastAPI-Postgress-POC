from typing import Optional
from urllib.request import Request
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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

myposts = [{
    "title": "title of post 1", "content": "content of post 1", "id": 1
},
    {
    "title": "favorite food", "content": "i like pizza", "id": 2
}]


def find_post(id):
    for p in myposts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(myposts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello Worldz"}


@app.get('/posts')
def get_posts():
    cursor.execute('select * from posts')
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    cursor.execute("""insert into posts(title, content, published) values(%s, %s, %s) 
    returning * """, (post.title, post.content, post.published))
    newpost = cursor.fetchone()
    conn.commit()

    return {'data': newpost}


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""select * from posts where id=%s 
     """, (str(id)))
    newpost = cursor.fetchone()

    return {'data': newpost}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    myposts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    post_dict = post.dict()
    post_dict['id'] = id
    myposts[index] = post_dict
    return {'data': post_dict}
