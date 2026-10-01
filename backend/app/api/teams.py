from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.stats import catelo_history, seasons, standings
from app.sports.config import SPORTS

router = APIRouter()


@router.get("/{sport}/seasons")
def get_seasons(sport: str, db: Session = Depends(get_db)):
    config = SPORTS[sport]
    return seasons(db, config)


@router.get("/{sport}/seasons/{season}/teams")
def get_teams(sport: str, season: int, db: Session = Depends(get_db)):
    config = SPORTS[sport]
    return standings(db, config, season)


@router.get("/{sport}/seasons/{season}/teams/{abbreviation}")
def get_team(sport: str, season: int, abbreviation: str, db: Session = Depends(get_db)):
    config = SPORTS[sport]
    team_model = config["team_model"]
    team = db.query(team_model).filter(team_model.abbreviation == abbreviation).one()
    history = catelo_history(db, config, team.id, season)
    return {
        "team": {
            "id": team.id,
            "name": team.name,
            "abbreviation": team.abbreviation,
            "current_catelo": history[-1]["catelo"] if history else None,
        },
        "history": history,
    }
