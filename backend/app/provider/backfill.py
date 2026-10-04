import argparse
import time
from datetime import date

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


def _mark_games_past_regular_season(session, config, season):
    game_model = config["game_model"]
    games = session.query(game_model).filter(game_model.season == season).order_by(game_model.date, game_model.id).all()

    played = {}
    for game in games:
        played[game.away_team_id] = played.get(game.away_team_id, 0) + 1
        played[game.home_team_id] = played.get(game.home_team_id, 0) + 1
        if played[game.home_team_id] > config["regular_season_games"]:
            game.postseason = True


def ingest_games(sport, season=None, dates=None, request_delay=60):
    config = SPORTS[sport]
    team_model = config["team_model"]
    game_model = config["game_model"]

    added_count = 0
    skipped_count = 0
    excluded_count = 0
    added_season = None
    cursor = None

    with SessionLocal() as session:
        while True:
            print(f"[{sport}] Fetching next page...")
            games_page = list_games(sport, 100, season=season, cursor=cursor, dates=dates)
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
                        season=game_data["season"],
                        date=date.fromisoformat(game_data["date"][:10]),
                        postseason=bool(game_data.get("postseason")),
                        **fields["game"],
                    )
                )
                added_count += 1
                added_season = game_data["season"]

            session.commit()
            cursor = games_page["meta"].get("next_cursor")
            if not cursor:
                break
            time.sleep(request_delay)

        if added_season:
            _mark_games_past_regular_season(session, config, added_season)
        session.commit()

        print(
            f"[{sport}] Done. Added {added_count} games, skipped {skipped_count} non-final, excluded {excluded_count}."
        )
        return added_count


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
