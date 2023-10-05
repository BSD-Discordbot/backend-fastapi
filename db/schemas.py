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

class CardUpgradeBase(BaseModel):
    amount: int
    requirement: int

class CardUpgrade(CardUpgradeBase):
    pass

class CardBase(BaseModel):
    name: str
    rarity: int
    tags: List[TagList] = []
    def tags_ids(self) -> List[int]:
        return [tag.id for tag in self.tags]
    upgrades: List["CardUpgrade"] = []
    class Config:
        from_attributes = True

class Card(CardBase):
    id: int