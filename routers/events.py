from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from dependencies import get_db

from db import crud, models, schemas

router = APIRouter()

@router.get("/events", response_model=list[schemas.Event], tags=['events'])
def read_all_events(db: Session = Depends(get_db)):
    events = crud.get_all_events(db)
    return events

@router.post('/events', response_model=schemas.Event, tags=['events'])
def create_event(event: schemas.EventBase, db: Session = Depends(get_db)):
    db_event = crud.create_event(db, event)
    return db_event

@router.put('/events/{event_id}', response_model=schemas.Event, tags=['events'])
def update_event(event_id: int, event: schemas.EventBase, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id)
    if(db_event == None):
        raise HTTPException(status_code=404, detail="Event not found")
    db_events = crud.update_event(db, event, db_event)
    return db_events

@router.delete('/events/{event_id}', tags=['events'])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    crud.delete_event(db, event_id)
    return

