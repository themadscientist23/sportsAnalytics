import argparse
import time
from datetime import datetime

from db.session import close_session, get_db_session
from sports_config import SPORTS


def _create_or_update_team(session, team_model, team_data):
    team = session.get(team_model, team_data["id"])
    if team is None:
        team = team_model(id=team_data["id"])
        session.add(team)
    team.name = team_data["name"]
    team.abbreviation = team_data["abbreviation"]


def ingest_games(sport, season, dates=None, request_delay=60):
    config = SPORTS[sport]
    games_api = config["games_api"]()
    team_model = config["team_model"]
    game_model = config["game_model"]

    session = get_db_session()
    added_count = 0
    skipped_count = 0
    cursor = None

    try:
        while True:
            print(f"[{sport}:{season}] Fetching next page...")
            games_page = games_api.list(seasons=[season], per_page=100, cursor=cursor, dates=dates)
            page_games = games_page.data
            if not page_games:
                break

            for g in page_games:
                game_data = g.model_dump()

                if not config["is_final"](game_data):
                    skipped_count += 1
                    continue

                game_id = game_data["id"]
                if session.get(game_model, game_id):
                    continue

                fields = config["extract"](game_data)
                _create_or_update_team(session, team_model, fields["home_team"])
                _create_or_update_team(session, team_model, fields["away_team"])

                session.add(game_model(
                    id=game_id,
                    season=season,
                    date=datetime.strptime(game_data["date"][:10], "%Y-%m-%d").date(),
                    postseason=bool(game_data.get("postseason")),
                    home_team_id=fields["home_team"]["id"],
                    away_team_id=fields["away_team"]["id"],
                    home_score=fields["home_score"],
                    away_score=fields["away_score"],
                ))
                added_count += 1

            session.commit()
            cursor = games_page.meta.next_cursor
            if not cursor:
                break
            time.sleep(request_delay)

        print(f"[{sport}:{season}] Done. Added {added_count} games, skipped {skipped_count} non-final.")
        return added_count

    except Exception as e:
        session.rollback()
        print(f"[{sport}:{season}] Error: {e}")
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

    ingest_games(args.sport, args.season, request_delay=args.request_delay)
