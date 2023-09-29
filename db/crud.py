from sqlalchemy.orm import Session

from . import models, schemas

def get_all_cards(db: Session):
    return db.query(models.Card).all()

def create_card(db: Session, card: schemas.CardBase):
    db_card = models.Card(**card)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, id: int):
    db.query(models.Card).filter(models.Card.id == id).delete()

def get_all_tags(db: Session):
    return db.query(models.Tag).all()

def create_tag(db: Session, tag: schemas.TagBase):
    db_tag = models.Tag(**tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, id: int):
    db.query(models.Tag).filter(models.Tag.id == id).delete()

def get_all_players(db: Session):
    return db.query(models.Player).all()

def get_player(db: Session, player_id: str):
    return db.query(models.Player).filter(models.Player.discord_id == player_id).first()