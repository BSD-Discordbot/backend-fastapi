from typing import BinaryIO, List
from sqlalchemy.orm import Session

from . import models, schemas

def get_all_cards(db: Session):
    cards = db.query(models.Card).all()
    return cards

def create_card(db: Session, card: schemas.CardBase):
    db_card = models.Card(**card)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def update_card(db: Session, card: schemas.CardBase):
    db_card = get_card(db, card.name)
    db_card.tags.clear()
    for tag in card.tags:
        db_card.tags.append(get_tag(db, tag.id))
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, name: str):
    card = get_card(db, name)
    db.delete(card)
    return db.commit()

def get_card(db: Session, name: str):
    return db.query(models.Card).filter(models.Card.name == name).first()

def set_card_image(db: Session, name: int, image: BinaryIO):
    card = get_card(db, name)
    card.image = image
    db.commit()

def get_all_tags(db: Session):
    return db.query(models.Tag).all()

def get_tag(db: Session, tag: int):
    return db.query(models.Tag).filter(models.Tag.id == tag).first()

def create_tag(db: Session, tag: schemas.TagBase):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, id: int):
    tag = get_tag(db, id)
    db.delete(tag)
    return db.commit()

def get_all_players(db: Session):
    return db.query(models.Player).all()

def get_player(db: Session, player_id: str):
    return db.query(models.Player).filter(models.Player.discord_id == player_id).first()