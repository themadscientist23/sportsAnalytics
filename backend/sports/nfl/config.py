from provider.api_client import api
from sports.nfl.models import NFLGame, NFLGameRating, NFLTeam
from sports.nfl.process_games import process_game


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


NFL_CONFIG = {
    "team_model": NFLTeam,
    "game_model": NFLGame,
    "rating_model": NFLGameRating,
    "games_api": lambda: api.nfl.games,
    "is_final": lambda g: g.get("status") == "Final",
    "extract": _extract,
    "process_game": process_game,
    "current_season": 2026,
}
