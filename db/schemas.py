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

class TagList(TagBase):
    id: int

class Tag(TagList):
    id: int
    cards: List['Card'] = []

    class Config:
        from_attributes = True


class CardBase(BaseModel):
    name: str
    rarity: int

class CardList(CardBase):
    id: int
    tags: List[Tag] = []

    class Config:
        from_attributes = True

class Card(CardList):
    upgrades: List["CardUpgrade"] = []

class CardUpgradeBase(BaseModel):
    amount: int
    requirement: Card

class CardUpgrade(CardUpgradeBase):
    pass