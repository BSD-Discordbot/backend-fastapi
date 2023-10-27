from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from dependencies import check_admin, get_db

from db import crud, schemas

router = APIRouter()

@router.get("/events", response_model=list[schemas.Event], tags=['events'])
def read_all_events(db: Session = Depends(get_db)):
    events = crud.get_all_events(db)
    return events

@router.post('/events', response_model=schemas.Event, dependencies=[Depends(check_admin)], tags=['events'])
def create_event(event: schemas.EventBase, db: Session = Depends(get_db)):
    db_event = crud.create_event(db, event)
    return db_event

@router.put('/events/{event_id}', response_model=schemas.Event, dependencies=[Depends(check_admin)], tags=['events'])
def update_event(event_id: int, event: schemas.EventBase, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id)
    if(db_event == None):
        raise HTTPException(status_code=404, detail="Event not found")
    db_events = crud.update_event(db, event, db_event)
    return db_events

@router.delete('/events/{event_id}', dependencies=[Depends(check_admin)], tags=['events'])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    crud.delete_event(db, event_id)
    return

