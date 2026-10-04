import requests

from app.core.config import BALLDONTLIE_API_KEY

BASE_URL = "https://api.balldontlie.io"


def list_games(sport, per_page, season=None, cursor=None, dates=None):
    response = requests.get(
        f"{BASE_URL}/{sport}/v1/games",
        headers={"Authorization": BALLDONTLIE_API_KEY},
        params={"seasons[]": season, "per_page": per_page, "cursor": cursor, "dates[]": dates},
    )
    response.raise_for_status()
    return response.json()
