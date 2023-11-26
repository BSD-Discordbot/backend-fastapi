import math
from fastapi import APIRouter, Request, Response, UploadFile
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from PIL import Image
from io import BytesIO

from dependencies import check_admin, get_db

from db import crud, schemas

from db.database import SessionLocal

router = APIRouter()

temp_io = BytesIO()

def generate_atlas(cards: list[schemas.Card]):
    cards.sort(key=lambda c: c.name)
    nmbWidth = math.floor(math.sqrt(cards.__len__()))
    nmbheight = math.ceil(cards.__len__()/nmbWidth)

    atlas = Image.new('RGBA', (nmbWidth*288, nmbheight*450))
    for index, card in enumerate(cards):
        if(card.image != None):
            x = (index%nmbWidth)*288
            y = (math.floor(index/nmbWidth))*450
            img = Image.open(BytesIO(card.image)).resize((288, 450))
            atlas.paste(img, (x, y, x+288, y+450))
    atlas.save(temp_io, format="PNG")
    print('Atlas Generated')
db_temp = SessionLocal()
cards = crud.get_all_cards(db_temp)
if(cards.__len__() > 0):
    generate_atlas(crud.get_all_cards(db_temp))
    db_temp.close()
else:
    print('No Atlas generated : no cards found')

@router.get("/cards", response_model=list[schemas.Card], tags=['cards'])
def read_all_cards(request: Request, db: Session = Depends(get_db)):
    cards = crud.get_all_cards(db)
    return cards

@router.put('/cards/{card_name}', response_model=schemas.Card, dependencies=[Depends(check_admin)], tags=['cards'])
def create_or_update_card(card_name: str, card: schemas.Card, db: Session = Depends(get_db)):
    db_card = crud.get_card(db, card_name)
    if(db_card == None):
        db_card = crud.create_card(db, card)
    else:
        db_card = crud.update_card(db, card, db_card)
    return db_card

@router.get('/cards/{card_name}', response_model=schemas.Card, tags=['cards'])
def read_card(card_name: str, db: Session = Depends(get_db)):
    db_card = crud.get_card(db, card_name)
    return db_card

@router.put('/cards/{card_name}/image', dependencies=[Depends(check_admin)], tags=['cards'])
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

@router.delete('/cards/{card_name}', dependencies=[Depends(check_admin)] ,tags=['cards'])
def delete_card(card_name: str, db: Session = Depends(get_db)):
    crud.delete_card(db, card_name)
    return

@router.get('/atlas', response_model=bytes, tags=['cards'])
def get_cards_atlas(db: Session= Depends(get_db)):
    if(temp_io.tell() == 0):
        raise HTTPException(status_code=404, detail="Atlas not generated")
    return Response(content=temp_io.getvalue(), media_type="image/png")