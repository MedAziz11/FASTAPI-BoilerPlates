#file from tiangolo

from app.core.database import Base

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


ModelType = TypeVar('ModelType', bound=Base) # our model should be a defined models from our models folder
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
# our schema must be a defined schema


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model:Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model
        
    def get(self, db: Session, id:Any)->Optional[ModelType]:
        """get a single element from a table By id"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        '''get multi rows from a table '''
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        '''creates an Object in a specific table'''
        
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        
        '''updates an specific row from a table'''
        
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        '''removes a specific row from a table'''
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
        