from fastapi import APIRouter, Response, UploadFile
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from dependencies import get_db

from db import crud, schemas

router = APIRouter()

@router.get("/cards", response_model=list[schemas.CardBase], tags=['cards'])
def read_all_cards(db: Session = Depends(get_db)):
    cards = crud.get_all_cards(db)
    return cards

@router.put('/cards/{card_name}', response_model=schemas.CardBase, tags=['cards'])
def create_or_update_card(card_name: str, card: schemas.CardBase, db: Session = Depends(get_db)):
    db_card = crud.get_card(db, card_name)
    if(db_card == None):
        db_card = crud.create_card(db, card)
    else:
        db_card = crud.update_card(db, card, db_card)
    return db_card

@router.get('/cards/{card_name}', response_model=schemas.CardBase, tags=['cards'])
def read_card(card_name: str, db: Session = Depends(get_db)):
    db_card = crud.get_card(db, card_name)
    return db_card

@router.put('/cards/{card_name}/image', tags=['cards'])
def set_card_image(card_name: str, file: UploadFile, db: Session = Depends(get_db)):
    card = crud.get_card(db, card_name)
    if(card == None):
        raise HTTPException(status_code=404, detail="Card not found")
    image = file.file.read()
    crud.set_card_image(db, card_name, image)
    return

@router.get('/cards/{card_name}/image', response_model=bytes, tags=['cards'])
def read_card_image(card_name: str, db: Session = Depends(get_db)):
    card = crud.get_card(db, card_name)
    if(card == None):
        raise HTTPException(status_code=404, detail="Card not found")
    if(card.image == None):
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=card.image, media_type="image/png")

@router.delete('/cards/{card_name}', tags=['cards'])
def delete_card(card_name: str, db: Session = Depends(get_db)):
    crud.delete_card(db, card_name)
    return