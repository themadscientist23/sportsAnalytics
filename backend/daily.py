import argparse
from datetime import datetime, timedelta

from backfill import ingest_games
from sports_config import SPORTS


def daily_update(sport, request_delay=60):
    config = SPORTS[sport]
    season = config["current_season"]

    today = datetime.today().date()
    start_date = today - timedelta(days=2)
    date_range = [(start_date + timedelta(days=i)).isoformat() for i in range((today - start_date).days + 1)]

    return ingest_games(sport, season, request_delay=request_delay, dates=date_range)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch the last 2 days of games for a sport's current season.")
    parser.add_argument("sport", choices=SPORTS.keys())
    parser.add_argument("--request-delay", type=float, default=60)
    args = parser.parse_args()

    added = daily_update(args.sport, request_delay=args.request_delay)
    print(f"{datetime.now()}: Daily {args.sport.upper()} update complete. {added} new games added.")
