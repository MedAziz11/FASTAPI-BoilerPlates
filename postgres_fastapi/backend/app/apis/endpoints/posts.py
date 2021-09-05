from typing import List, Any
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.schemas.post import PostResponse, PostSchema
from app.models import posts
from app.apis import deps


router = APIRouter()

@router.get("/", response_model=List[PostResponse])
async def get_posts(db:Session = Depends(deps.get_db))-> Any:
    db_posts = db.query(posts.Post).all()
    
    return db_posts

@router.post("/", response_model=PostResponse)
async def add_post(*, 
                   db: Session = Depends(deps.get_db),
                   post_in: PostSchema)->Any:
    post = posts.Post(**jsonable_encoder(post_in))
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
    
