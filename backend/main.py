from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from db import get_db

app = FastAPI(title= "Sports Analytics API")

conn, cursor = get_db()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return RedirectResponse(url='/teams')


@app.get("/teams")
def get_teams():
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    return {"teams": teams}


