from database_config import api
from nfl.models import NFLGame, NFLGameRating, NFLTeam


def _extract(game):
    home, away = game["home_team"], game["visitor_team"]
    return {
        "home_team": {"id": home["id"], "name": home["full_name"], "abbreviation": home["abbreviation"]},
        "away_team": {"id": away["id"], "name": away["full_name"], "abbreviation": away["abbreviation"]},
        "home_score": int(game["home_team_score"]),
        "away_score": int(game["visitor_team_score"]),
    }


NFL_CONFIG = {
    "team_model": NFLTeam,
    "game_model": NFLGame,
    "rating_model": NFLGameRating,
    "games_api": lambda: api.nfl.games,
    "is_final": lambda g: g.get("status") == "Final",
    "extract": _extract,
    "current_season": 2026,
    "home_advantage": 50,
}
