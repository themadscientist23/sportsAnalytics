from provider.api_client import api
from sports.mlb.models import MLBGame, MLBGameRating, MLBTeam


def _extract(game):
    home, away = game["home_team"], game["away_team"]
    return {
        "home_team": {"id": home["id"], "name": home["display_name"], "abbreviation": home["abbreviation"]},
        "away_team": {"id": away["id"], "name": away["display_name"], "abbreviation": away["abbreviation"]},
        "home_score": int(game["home_team_data"]["runs"]),
        "away_score": int(game["away_team_data"]["runs"]),
    }


MLB_CONFIG = {
    "team_model": MLBTeam,
    "game_model": MLBGame,
    "rating_model": MLBGameRating,
    "games_api": lambda: api.mlb.games,
    "is_final": lambda g: g.get("status") == "STATUS_FINAL",
    "extract": _extract,
    "current_season": 2026,
    "home_advantage": 50,
}
