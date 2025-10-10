from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_config import get_db_session, close_session
from models import NBATeam, NFLTeam, MLBTeam

app = FastAPI(title="Sports Analytics API")

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
    return {"message": "Sports Analytics API is running."}


@app.get("/nbateams")
def get_nba_teams():
    session = get_db_session()
    teams = session.query(NBATeam).all()
    result = [
        {
            "id": t.id,
            "name": t.name,
            "wins": t.wins,
            "losses": t.losses,
            "points_for": t.points_for,
            "points_against": t.points_against,
            "catelo": t.catelo,
            "updated_at": t.updated_at
        }
        for t in teams
    ]
    close_session(session)
    return result


@app.get("/nflteams")
def get_nfl_teams():
    session = get_db_session()
    teams = session.query(NFLTeam).all()
    result = [
        {
            "id": t.id,
            "name": t.name,
            "wins": t.wins,
            "losses": t.losses,
            "ties": t.ties,
            "points_for": t.points_for,
            "points_against": t.points_against,
            "catelo": t.catelo,
            "updated_at": t.updated_at,
            "abbreviation": t.abbreviation
        }
        for t in teams
    ]
    close_session(session)
    return result


@app.get("/mlbteams")
def get_mlb_teams():
    session = get_db_session()
    teams = session.query(MLBTeam).all()
    result = [
        {
            "id": t.id,
            "name": t.name,
            "wins": t.wins,
            "losses": t.losses,
            "points_for": t.points_for,
            "points_against": t.points_against,
            "catelo": t.catelo,
            "updated_at": t.updated_at
        }
        for t in teams
    ]
    close_session(session)
    return result