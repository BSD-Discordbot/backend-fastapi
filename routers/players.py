from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from dependencies import get_db

from db import crud, schemas

router = APIRouter()

@router.get('/players', response_model=list[schemas.PlayerList], tags=['players'])
def read_all_players(db: Session = Depends(get_db)):
    players = crud.get_all_players(db)
    return players

@router.get("/players/{player_id}", response_model=schemas.Player, tags=['players'])
def read_player_cards(player_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_player(db, player_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Player not found")
    return db_user