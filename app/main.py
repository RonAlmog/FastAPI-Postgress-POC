from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# create tables in db if they don't exist.
# this line is not needed if you're using alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# allow cors access from these domains:
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://mywebsitezyysszxxx.com"
]
# to allow every domain:
# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello Worldz"}
