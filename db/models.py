from sqlalchemy import Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import datetime
from typing import List

from .database import Base

association_table = Table(
    "player_has_cards",
    Base.metadata,
    Column("player", ForeignKey("player.discord_id"), primary_key=True),
    Column("card", ForeignKey("card.id"), primary_key=True),
    Column("amount", Integer, primary_key=True),
)

class Card(Base):
    __tablename__ = "card"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[int] = mapped_column(index=True, unique=True)
    rarity: Mapped[int] = mapped_column()

class Player(Base):
    __tablename__ = "player"
    discord_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    balance: Mapped[int] = mapped_column(default=0)
    last_daily: Mapped[datetime.datetime] = mapped_column(DateTime)
    daily_streak: Mapped[int] = mapped_column(Integer, default=0)
    cards: Mapped[List[Card]] = relationship(secondary=association_table)


# interface PlayerHasCard {
#   discord_id: bigint
#   card_id: number
#   amount: number
#   date_owned: Date
# }

    



# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
