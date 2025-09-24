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
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return RedirectResponse(url='/nbateams')


@app.get("/nbateams")
def get_teams():
    cursor.execute("SELECT * FROM nba_teams")
    rows = cursor.fetchall()
    teams = [
        {
            "id": row[0],
            "name": row[1],
            "wins": row[2],
            "losses": row[3],
            "win_percentage": row[4],
            "points_for": row[5],
            "points_against": row[6],
            "points_differential": row[7]
        }
        for row in rows
    ]
    return {"nba_teams": teams}

@app.get("/nflteams")
def get_teams():
    cursor.execute("SELECT * FROM nfl_teams")
    rows = cursor.fetchall()
    teams = [
        {
            "id": row[0],
            "name": row[1],
            "wins": row[2],
            "losses": row[3],
            "ties": row[4],
            "win_percentage": row[5],
            "points_for": row[6],
            "points_against": row[7],
            "points_differential": row[8]
        }
        for row in rows
    ]
    return {"nfl_teams": teams}


@app.get("/mlbteams")
def get_teams():
    cursor.execute("SELECT * FROM mlb_teams")
    rows = cursor.fetchall()
    teams = [
        {
            "id": row[0],
            "name": row[1],
            "wins": row[2],
            "losses": row[3],
            "win_percentage": row[4],
            "points_for": row[5],
            "points_against": row[6],
            "points_differential": row[7]
        }
        for row in rows
    ]
    return {"mlb_teams": teams}


