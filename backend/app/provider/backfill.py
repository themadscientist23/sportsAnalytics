import argparse
import time
from datetime import datetime

from app.db.session import SessionLocal
from app.provider.api_client import list_games
from app.sports.config import SPORTS


def _create_or_update_team(session, team_model, team_data):
    team = session.get(team_model, team_data["id"])
    if team is None:
        team = team_model(id=team_data["id"])
        session.add(team)
    team.name = team_data["name"]
    team.abbreviation = team_data["abbreviation"]


def _is_excluded(game_data, fields):
    return (
        game_data.get("season_type") == "spring_training"
        or game_data.get("ist_stage") == "Championship"
        or fields["home_team"]["id"] < 0
        or fields["away_team"]["id"] < 0
    )


def ingest_games(sport, season, dates=None, request_delay=60):
    config = SPORTS[sport]
    team_model = config["team_model"]
    game_model = config["game_model"]

    added_count = 0
    skipped_count = 0
    excluded_count = 0
    cursor = None

    with SessionLocal() as session:
        try:
            while True:
                print(f"[{sport}:{season}] Fetching next page...")
                games_page = list_games(sport, [season], 100, cursor=cursor, dates=dates)
                page_games = games_page["data"]
                if not page_games:
                    break

                for game_data in page_games:
                    if not config["is_final"](game_data):
                        skipped_count += 1
                        continue

                    game_id = game_data["id"]
                    if session.get(game_model, game_id):
                        continue

                    fields = config["extract"](game_data)
                    if _is_excluded(game_data, fields):
                        excluded_count += 1
                        continue

                    _create_or_update_team(session, team_model, fields["home_team"])
                    _create_or_update_team(session, team_model, fields["away_team"])

                    session.add(
                        game_model(
                            id=game_id,
                            season=season,
                            date=datetime.strptime(game_data["date"][:10], "%Y-%m-%d").date(),
                            postseason=bool(game_data.get("postseason")),
                            **fields["game"],
                        )
                    )
                    added_count += 1

                session.commit()
                cursor = games_page["meta"].get("next_cursor")
                if not cursor:
                    break
                time.sleep(request_delay)

            print(
                f"[{sport}:{season}] Done. Added {added_count} games, "
                f"skipped {skipped_count} non-final, excluded {excluded_count}."
            )
            return added_count

        except Exception as e:
            session.rollback()
            print(f"[{sport}:{season}] Error: {e}")
            raise


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
