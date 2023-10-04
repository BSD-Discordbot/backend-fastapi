from fastapi import APIRouter, UploadFile
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from dependencies import get_db

from db import crud, models, schemas

router = APIRouter()

@router.get("/cards", response_model=list[schemas.CardBase])
def read_all_cards(db: Session = Depends(get_db)):
    cards = crud.get_all_cards(db)
    return cards

@router.post('/cards/{card_id}', response_model=schemas.CardList)
def create_card(card: schemas.CardBase, db: Session = Depends(get_db)):
    db_card = crud.create_card(db, card)
    return db_card

@router.put('/cards/{card_id}', response_model=schemas.CardList)
def update_card(card: schemas.CardBase, db: Session = Depends(get_db)):
    db_card = crud.update_card(db, card)
    return db_card

@router.get('/cards/{card_id}', response_model=schemas.CardList)
def read_card(card_id: str, db: Session = Depends(get_db)):
    db_card = crud.get_card(db, card_id)
    return db_card

@router.put('/cards/{card_id}/image')
def set_card_image(card_id: str, file: UploadFile, db: Session = Depends(get_db)):
    card = crud.get_card(db, card_id)
    if(card == None):
        raise HTTPException(status_code=404, detail="Card not found")
    crud.set_card_image(db, card_id, file.file)
    return

@router.get('/cards/{card_id}/image', response_model=bytes)
def read_card_image(card_id: str, db: Session = Depends(get_db)):
    card = crud.get_card(db, card_id)
    if(card == None):
        raise HTTPException(status_code=404, detail="Card not found")
    if(card.image == None):
        raise HTTPException(status_code=404, detail="Image not found")
    return card.image

@router.delete('/cards/{card_id}')
def delete_card(card_id: str, db: Session = Depends(get_db)):
    crud.delete_card(db, card_id)
    return