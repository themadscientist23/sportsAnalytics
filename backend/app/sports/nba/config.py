from app.sports.nba.models import NBAGame, NBAGameRating, NBATeam
from app.sports.nba.process_games import process_game


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
    "is_final": lambda g: g.get("status") == "Final",
    "extract": _extract,
    "process_game": process_game,
    "current_season": 2025,
}
