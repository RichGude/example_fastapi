# Import libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote
from .config import settings

# For SQLAlchemy Modules
from . import models
from .database import engine

# Carry over the instance of SQLAlchemy (not needed when using Alembic)
# models.Base.metadata.create_all(bind=engine)

# Initiate an instance of FastAPI
app = FastAPI()

# Specify the domains from which the api is allowed to accept requests
origins = ['*']

# Middleware is a function that a request is passed through prior to any routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tie routers to main app file
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Deploy instance of FastAPI
@app.get("/")                   # Submit a get request at the localhost root path
async def root():
    # FastAPI automatically converts return values to JSON
    return {"message": "It is finished"}