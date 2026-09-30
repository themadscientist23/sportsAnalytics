from provider.api_client import api
from sports.nba.models import NBAGame, NBAGameRating, NBATeam


def _extract(game):
    home, away = game["home_team"], game["visitor_team"]
    return {
        "home_team": {"id": home["id"], "name": home["full_name"], "abbreviation": home["abbreviation"]},
        "away_team": {"id": away["id"], "name": away["full_name"], "abbreviation": away["abbreviation"]},
        "game": {
            "home_team_id": home["id"],
            "away_team_id": away["id"],
            "home_score": int(game["home_team_score"]),
            "away_score": int(game["visitor_team_score"]),
        },
    }


NBA_CONFIG = {
    "team_model": NBATeam,
    "game_model": NBAGame,
    "rating_model": NBAGameRating,
    "games_api": lambda: api.nba.games,
    "is_final": lambda g: g.get("status") == "Final",
    "extract": _extract,
    "current_season": 2025,
    "home_advantage": 50,
}
