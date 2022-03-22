
from pydantic import BaseModel
from datetime import datetime


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
