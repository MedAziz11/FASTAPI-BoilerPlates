from fastapi import APIRouter

from app.apis.endpoints import posts

api_router = APIRouter()

api_router.include_router(posts.router, prefix="/posts", tags=["posts"])