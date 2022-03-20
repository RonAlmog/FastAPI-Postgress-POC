from typing import Optional
from urllib.request import Request
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
    return {"data": myposts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    myposts.append(post_dict)

    return {'data': post_dict}


@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {'data': post}


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
