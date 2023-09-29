from typing import List
from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class Tag(TagBase):
    id: int
    cards: list["Card"] = []

    class Config:
        orm_mode = True

class CardBase(BaseModel):
    name: int
    rarity: int

class Card(CardBase):
    id: int
    tags: list["Tag"] = []
    upgrades: list["CardUpgrade"] = []
    upgrade_requirements: list["CardUpgrade"] = []

    class Config:
        orm_mode = True

class CardUpgradeBase(BaseModel):
    card: "Card"
    amount: int
    requirement: "Card"

class CardUpgrade(CardUpgradeBase):
    
    class Config:
        orm_mode = True