
import os
import requests
from fastapi import FastAPI, Depends, HTTPException, Request
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers import cards, players, tags, events

from dependencies import get_db

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

app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=604800, same_site="none", https_only=True)

def get_user_token(code:str):
    data = {
        "client_id": os.getenv("DISCORD_CLIENT_ID", ""),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET", ""),
        "code": code,
        'grant_type': 'authorization_code',
        "redirect_uri": os.getenv("API_URL", ""),
        "scope": 'identify',
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if(response.ok == False):
       raise HTTPException(status_code=500)
    return response.json()


app.include_router(cards.router)
app.include_router(players.router)
app.include_router(tags.router)
app.include_router(events.router)

@app.get('/login')
def login(request: Request, code: str):
    if(code == None):
        return RedirectResponse(url=os.getenv("FRONT_URL", ""))
    request.session['access_token'] = get_user_token(code)['access_token']
    return RedirectResponse(url=os.getenv("FRONT_URL", ""))

@app.get('/me')
def me(request: Request):
    token = request.session.get("access_token", None)
    if(token == None):
        raise HTTPException(status_code=401, detail="User not authentified")
    userinfo = requests.get('https://discord.com/api/users/@me', headers={'Authorization': 'Bearer '+token})
    data = userinfo.json()
    data['isAdmin'] = data['id'] == '268494575780233216'
    return data