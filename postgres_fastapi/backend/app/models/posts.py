from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey

from app.core.database import Base
from .user import User


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")
    content = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
