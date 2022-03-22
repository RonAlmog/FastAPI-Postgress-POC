
from urllib.parse import uses_fragment
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.database import Base


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

# return schema


class Post(PostBase):
    # other fields are inherited
    id: int
    created_at: datetime

    class Config():
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
