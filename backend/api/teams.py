from fastapi import APIRouter

from db.session import close_session, get_db_session
from db.stats import catelo_history, seasons, standings
from provider.sports_config import SPORTS

router = APIRouter()


@router.get("/{sport}/seasons")
def get_seasons(sport: str):
    config = SPORTS[sport]
    session = get_db_session()
    try:
        return seasons(session, config)
    finally:
        close_session(session)


@router.get("/{sport}/seasons/{season}/teams")
def get_teams(sport: str, season: int):
    config = SPORTS[sport]
    session = get_db_session()
    try:
        return standings(session, config, season)
    finally:
        close_session(session)


@router.get("/{sport}/seasons/{season}/teams/{abbreviation}")
def get_team(sport: str, season: int, abbreviation: str):
    config = SPORTS[sport]
    team_model = config["team_model"]
    session = get_db_session()
    try:
        team = session.query(team_model).filter(team_model.abbreviation == abbreviation).one()
        history = catelo_history(session, config, team.id, season)
        return {
            "team": {
                "id": team.id,
                "name": team.name,
                "abbreviation": team.abbreviation,
                "current_catelo": history[-1]["catelo"] if history else None,
            },
            "history": history,
        }
    finally:
        close_session(session)
