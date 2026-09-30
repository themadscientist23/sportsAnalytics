import argparse
import time
from datetime import datetime

from database_config import get_db_session, close_session, api
from models import (
    NBAGame, NBAGameDerived,
    NFLGame, NFLGameDerived,
    MLBGame, MLBGameDerived,
)


def _nba_nfl_extract(game):
    return {
        "home_team_abbr": game["home_team"]["abbreviation"],
        "away_team_abbr": game["visitor_team"]["abbreviation"],
        "home_score": game["home_team_score"],
        "away_score": game["visitor_team_score"],
    }


def _mlb_extract(game):
    return {
        "home_team_abbr": game["home_team"]["abbreviation"],
        "away_team_abbr": game["away_team"]["abbreviation"],
        "home_score": game["home_team_data"]["runs"],
        "away_score": game["away_team_data"]["runs"],
    }


SPORTS = {
    "nba": {
        "games_api": lambda: api.nba.games,
        "game_model": NBAGame,
        "derived_model": NBAGameDerived,
        "is_final": lambda g: g.get("status") == "Final",
        "extract": _nba_nfl_extract,
    },
    "nfl": {
        "games_api": lambda: api.nfl.games,
        "game_model": NFLGame,
        "derived_model": NFLGameDerived,
        "is_final": lambda g: g.get("status") == "Final",
        "extract": _nba_nfl_extract,
    },
    "mlb": {
        "games_api": lambda: api.mlb.games,
        "game_model": MLBGame,
        "derived_model": MLBGameDerived,
        "is_final": lambda g: g.get("status") == "STATUS_FINAL",
        "extract": _mlb_extract,
    },
}


def backfill(sport, season, request_delay=60):
    config = SPORTS[sport]
    games_api = config["games_api"]()
    game_model = config["game_model"]
    derived_model = config["derived_model"]

    session = get_db_session()
    added_count = 0
    skipped_count = 0
    cursor = None

    try:
        while True:
            print(f"[{sport}:{season}] Fetching next page...")
            games_page = games_api.list(seasons=[season], per_page=100, cursor=cursor)
            page_games = games_page.data
            if not page_games:
                break

            for g in page_games:
                game_data = g.model_dump()

                if not config["is_final"](game_data) or game_data.get("postseason"):
                    skipped_count += 1
                    continue

                game_id = game_data["id"]
                if session.query(game_model.id).filter(game_model.id == game_id).first():
                    continue

                game_date = datetime.strptime(game_data["date"][:10], "%Y-%m-%d").date()
                fields = config["extract"](game_data)

                session.add(game_model(id=game_id, season=season, date=game_date, **fields))
                session.add(derived_model(game_id=game_id, processed=False))
                added_count += 1

            session.commit()
            cursor = games_page.meta.next_cursor
            if not cursor:
                break
            time.sleep(request_delay)

        print(f"[{sport}:{season}] Done. Added {added_count} games, skipped {skipped_count} non-final/postseason.")
        return added_count

    except Exception as e:
        session.rollback()
        print(f"[{sport}:{season}] Error during backfill: {e}")
        raise
    finally:
        close_session(session)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill historical games for a sport/season.")
    parser.add_argument("sport", choices=SPORTS.keys())
    parser.add_argument("season", type=int)
    parser.add_argument(
        "--request-delay",
        type=float,
        default=60,
        help="Seconds to sleep between paginated API requests",
    )
    args = parser.parse_args()

    backfill(args.sport, args.season, request_delay=args.request_delay)
