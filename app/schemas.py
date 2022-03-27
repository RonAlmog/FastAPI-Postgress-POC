
from urllib.parse import uses_fragment
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.database import Base


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

# return schema


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        orm_mode = True


class Post(PostBase):
    # other fields are inherited
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config():
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int       # 0=down, 1=up
