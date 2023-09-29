from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from dependencies import get_db

from db import crud, models, schemas

router = APIRouter()

@router.get('/players', response_model=list[schemas.PlayerList])
def read_all_players(db: Session = Depends(get_db)):
    players = crud.get_all_players(db)
    return players

@router.get("/players/{player_id}/cards", response_model=list[schemas.CardList])
def read_player_cards(player_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_player(db, player_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Player not found")
    cards = db_user.cards
    return cards