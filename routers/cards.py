from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from dependencies import get_db

from db import crud, models, schemas

router = APIRouter()

@router.get("/cards", response_model=list[schemas.Card])
def read_all_cards(db: Session = Depends(get_db)):
    cards = crud.get_all_cards(db)
    return cards

@router.post('/cards', response_model=schemas.CardList)
def create_card(card: schemas.CardBase, db: Session = Depends(get_db)):
    db_card = crud.create_card(db, card)
    return db_card

@router.delete('/cards/{card_id}')
def delete_tag(card_id: int, db: Session = Depends(get_db)):
    crud.delete_card(db, card_id)
    return