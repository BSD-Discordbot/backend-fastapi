from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from dependencies import get_db

from db import crud, models, schemas

router = APIRouter()

@router.get("/tags", response_model=list[schemas.TagList])
def read_tags(db: Session = Depends(get_db)):
    tags = crud.get_all_tags(db)
    return tags

@router.post('/tags', response_model=schemas.TagList)
def create_card(tag: schemas.TagBase, db: Session = Depends(get_db)):
    db_tag = crud.create_tag(db, tag)
    return db_tag

@router.delete('/tags/{tag_id}')
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    crud.delete_tag(db, tag_id)
    return

