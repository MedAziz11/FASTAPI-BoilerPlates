from fastapi import APIRouter

from app.apis.endpoints import posts, user

api_router = APIRouter()

api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(user.router, prefix="/user", tags=["user"])