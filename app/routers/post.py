from .. import schemas, models, oauth2
from typing import Optional, List
from urllib.request import Request
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), userid: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createpost(post: schemas.PostCreate, db: Session = Depends(get_db), userid: int = Depends(oauth2.get_current_user)):
    newpost = models.Post(**post.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    # print(userid)

    return newpost


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), userid: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), userid: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), userid: int = Depends(oauth2.get_current_user)):

    postquery = db.query(models.Post).filter(models.Post.id == id)
    post = postquery.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    postquery.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return postquery.first()
