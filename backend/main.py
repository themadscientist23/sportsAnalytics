from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload
from database_config import get_db_session, close_session
from models import (
    NBATeam, NFLTeam, MLBTeam,
    NBAGame, NBAGameDerived,
    NFLGame, NFLGameDerived,
    MLBGame, MLBGameDerived
)

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
            "abbreviation": t.abbreviation,
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
            "abbreviation": t.abbreviation,
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


@app.get("/nba/team/{abbreviation}/catelo-history")
def get_nba_team_catelo_history(abbreviation: str):
    session = get_db_session()
    try:
        team = session.query(NBATeam).filter(NBATeam.abbreviation == abbreviation).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        # Get all games where this team played (home or away)
        home_games = (
            session.query(NBAGameDerived, NBAGame)
            .join(NBAGame, NBAGameDerived.game_gid == NBAGame.gid)
            .filter(NBAGame.home_team_abbr == abbreviation)
            .filter(NBAGameDerived.processed == True)
            .order_by(NBAGame.date)
            .all()
        )
        
        away_games = (
            session.query(NBAGameDerived, NBAGame)
            .join(NBAGame, NBAGameDerived.game_gid == NBAGame.gid)
            .filter(NBAGame.away_team_abbr == abbreviation)
            .filter(NBAGameDerived.processed == True)
            .order_by(NBAGame.date)
            .all()
        )
        
        history = []
        for derived, game in home_games:
            history.append({
                "date": game.date.isoformat(),
                "catelo": derived.home_post_catelo,
                "opponent": game.away_team_abbr,
                "home": True,
                "score": f"{game.home_score}-{game.away_score}"
            })
        
        for derived, game in away_games:
            history.append({
                "date": game.date.isoformat(),
                "catelo": derived.away_post_catelo,
                "opponent": game.home_team_abbr,
                "home": False,
                "score": f"{game.away_score}-{game.home_score}"
            })
        
        # Sort by date
        history.sort(key=lambda x: x["date"])
        
        return {
            "team": {
                "id": team.id,
                "name": team.name,
                "abbreviation": team.abbreviation,
                "current_catelo": team.catelo
            },
            "history": history
        }
    finally:
        close_session(session)


@app.get("/nfl/team/{abbreviation}/catelo-history")
def get_nfl_team_catelo_history(abbreviation: str):
    session = get_db_session()
    try:
        team = session.query(NFLTeam).filter(NFLTeam.abbreviation == abbreviation).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        # Get all games where this team played (home or away)
        home_games = (
            session.query(NFLGameDerived, NFLGame)
            .join(NFLGame, NFLGameDerived.game_id == NFLGame.id)
            .filter(NFLGame.home_team_abbr == abbreviation)
            .filter(NFLGameDerived.processed == True)
            .order_by(NFLGame.date)
            .all()
        )
        
        away_games = (
            session.query(NFLGameDerived, NFLGame)
            .join(NFLGame, NFLGameDerived.game_id == NFLGame.id)
            .filter(NFLGame.away_team_abbr == abbreviation)
            .filter(NFLGameDerived.processed == True)
            .order_by(NFLGame.date)
            .all()
        )
        
        history = []
        for derived, game in home_games:
            history.append({
                "date": game.date.isoformat(),
                "catelo": derived.home_post_catelo,
                "opponent": game.away_team_abbr,
                "home": True,
                "score": f"{game.home_score}-{game.away_score}"
            })
        
        for derived, game in away_games:
            history.append({
                "date": game.date.isoformat(),
                "catelo": derived.away_post_catelo,
                "opponent": game.home_team_abbr,
                "home": False,
                "score": f"{game.away_score}-{game.home_score}"
            })
        
        # Sort by date
        history.sort(key=lambda x: x["date"])
        
        return {
            "team": {
                "id": team.id,
                "name": team.name,
                "abbreviation": team.abbreviation,
                "current_catelo": team.catelo
            },
            "history": history
        }
    finally:
        close_session(session)


@app.get("/mlb/team/{abbreviation}/catelo-history")
def get_mlb_team_catelo_history(abbreviation: str):
    session = get_db_session()
    try:
        team = session.query(MLBTeam).filter(MLBTeam.abbreviation == abbreviation).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        # Get all games where this team played (home or away)
        home_games = (
            session.query(MLBGameDerived, MLBGame)
            .join(MLBGame, MLBGameDerived.game_id == MLBGame.id)
            .filter(MLBGame.home_team_abbr == abbreviation)
            .filter(MLBGameDerived.processed == True)
            .order_by(MLBGame.date)
            .all()
        )
        
        away_games = (
            session.query(MLBGameDerived, MLBGame)
            .join(MLBGame, MLBGameDerived.game_id == MLBGame.id)
            .filter(MLBGame.away_team_abbr == abbreviation)
            .filter(MLBGameDerived.processed == True)
            .order_by(MLBGame.date)
            .all()
        )
        
        history = []
        for derived, game in home_games:
            history.append({
                "date": game.date.isoformat(),
                "catelo": derived.home_post_catelo,
                "opponent": game.away_team_abbr,
                "home": True,
                "score": f"{game.home_score}-{game.away_score}"
            })
        
        for derived, game in away_games:
            history.append({
                "date": game.date.isoformat(),
                "catelo": derived.away_post_catelo,
                "opponent": game.home_team_abbr,
                "home": False,
                "score": f"{game.away_score}-{game.home_score}"
            })
        
        # Sort by date
        history.sort(key=lambda x: x["date"])
        
        return {
            "team": {
                "id": team.id,
                "name": team.name,
                "abbreviation": team.abbreviation,
                "current_catelo": team.catelo
            },
            "history": history
        }
    finally:
        close_session(session)