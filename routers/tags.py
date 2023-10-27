from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from dependencies import check_admin, get_db

from db import crud, models, schemas

router = APIRouter()

@router.get("/tags", response_model=list[schemas.TagList], tags=['tags'])
def read_all_tags(db: Session = Depends(get_db)):
    tags = crud.get_all_tags(db)
    return tags

@router.post('/tags', response_model=schemas.TagList, dependencies=[Depends(check_admin)], tags=['tags'])
def create_tag(tag: schemas.TagBase, db: Session = Depends(get_db)):
    db_tag = crud.create_tag(db, tag)
    return db_tag

@router.delete('/tags/{tag_id}', dependencies=[Depends(check_admin)], tags=['tags'])
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    crud.delete_tag(db, tag_id)
    return

