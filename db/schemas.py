from datetime import datetime
from typing import List
from pydantic import BaseModel

class PlayerBase(BaseModel):
    discord_id: str

class PlayerList(PlayerBase):
    balance: int
    last_daily: datetime
    daily_streak: int

class Player(PlayerList):
    cards: List['Card'] = []

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class TagList(TagBase):
    id: int
    name: str

class Tag(TagList):
    cards: List['Card'] = []

    class Config:
        from_attributes = True

class CardBase(BaseModel):
    name: str
    rarity: int
    tags: List[TagList] = []

class CardList(CardBase):
    id: int
    class Config:
        from_attributes = True

class Card(CardList):
    upgrades: List["CardUpgrade"] = []

class CardUpgradeBase(BaseModel):
    amount: int
    requirement: Card

class CardUpgrade(CardUpgradeBase):
    pass