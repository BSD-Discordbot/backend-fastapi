
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import cards, players, tags, events

app = FastAPI()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cards.router)
app.include_router(players.router)
app.include_router(tags.router)
app.include_router(events.router)