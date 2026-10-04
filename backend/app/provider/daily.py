import argparse
import logging
from datetime import datetime, timedelta

from app.provider.backfill import ingest_games
from app.sports.config import SPORTS

logger = logging.getLogger(__name__)


def daily_update(sport, request_delay=60):
    today = datetime.today().date()
    start_date = today - timedelta(days=2)
    date_range = [(start_date + timedelta(days=i)).isoformat() for i in range((today - start_date).days + 1)]

    return ingest_games(sport, dates=date_range, request_delay=request_delay)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Fetch the last 2 days of games for a sport.")
    parser.add_argument("sport", choices=SPORTS.keys())
    parser.add_argument("--request-delay", type=float, default=60)
    args = parser.parse_args()

    added = daily_update(args.sport, request_delay=args.request_delay)
    logger.info(f"Daily {args.sport.upper()} update complete. {added} new games added.")
