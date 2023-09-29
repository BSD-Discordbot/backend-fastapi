from sqlalchemy import Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import datetime
from typing import List
from typing import Optional

from .database import Base

player_has_cards = Table(
    "player_has_cards",
    Base.metadata,
    Column("player", ForeignKey("player.discord_id"), primary_key=True),
    Column("card", ForeignKey("card.id"), primary_key=True),
    Column("amount", Integer, primary_key=True),
)

card_has_tags = Table(
    "card_has_tags",
    Base.metadata,
    Column("card", ForeignKey("card.id"), primary_key=True),
    Column("tag", ForeignKey("tag.id"), primary_key=True),
)

event_has_cards = Table(
    "event_has_cards",
    Base.metadata,
    Column("event", ForeignKey("event.id"), primary_key=True),
    Column("card", ForeignKey("card.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    cards: Mapped[List["Card"]] = relationship(secondary=card_has_tags, back_populates="tags")

class Card(Base):
    __tablename__ = "card"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[int] = mapped_column(index=True, unique=True)
    rarity: Mapped[int] = mapped_column(nullable=False)
    tags: Mapped[List[Tag]] = relationship(secondary=card_has_tags, back_populates="cards")
    upgrades: Mapped[List["CardUpgrade"]] = relationship(back_populates="card", foreign_keys="CardUpgrade.card_id")
    upgrade_requirements: Mapped[List["CardUpgrade"]] = relationship(back_populates="requirement", foreign_keys="CardUpgrade.requirement_id")
    
class Player(Base):
    __tablename__ = "player"
    discord_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    balance: Mapped[int] = mapped_column(default=0)
    last_daily: Mapped[datetime.datetime] = mapped_column(DateTime)
    daily_streak: Mapped[int] = mapped_column(Integer, default=0)
    cards: Mapped[List[Card]] = relationship(secondary=player_has_cards)

class CardUpgrade(Base):
    __tablename__ = "card_upgrade"
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"), primary_key=True, index=True)
    card: Mapped["Card"] = relationship(back_populates="upgrades", foreign_keys="CardUpgrade.card_id")
    amount: Mapped[int] = mapped_column(default=1)
    requirement_id: Mapped[int] = mapped_column(ForeignKey("card.id"), primary_key=True)
    requirement: Mapped["Card"] = relationship(back_populates="upgrade_requirements", foreign_keys="CardUpgrade.requirement_id")

# interface Event {
#   id: Generated<number>
#   start_time?: number
#   end_time?: number
#   name: string
#   default: boolean
# }
class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column()
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column()
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    default: Mapped[bool] = mapped_column(nullable=False, default=False)
    cards: Mapped[List[Card]] = relationship(secondary=event_has_cards)
