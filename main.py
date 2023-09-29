
from fastapi import FastAPI

from routers import cards, players, tags

app = FastAPI()

app.include_router(cards.router)
app.include_router(players.router)
app.include_router(tags.router)