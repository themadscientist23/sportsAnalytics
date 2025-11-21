import time
from datetime import datetime
from database_config import get_db_session, close_session, api
from models import NFLGame, NFLGameDerived

SEASON = 2025
ENDDATE = "2025-04-13"
api_cursor = None

def populate_all_nfl_games():
    session = get_db_session()
    skipped_count = 0
    added_count = 0

    try:
        while True:
            print("Fetching next page...")
            time.sleep(60)
            games_page = api.nfl.games.list(
                seasons=[SEASON],
                per_page=100,
                cursor=api_cursor,
                end_date=ENDDATE
            )
            page_games = games_page.data
            if not page_games:
                break

            for g in page_games:
                game_data = g.model_dump()

                if game_data.get("status") != "Final" or game_data.get("postseason"):
                    skipped_count += 1
                    continue

                game_id = game_data.get("id")
                game_date = datetime.strptime(game_data.get("date"), "%Y-%m-%d").date()
                home_team_abbr = game_data.get("home_team", {}).get("abbreviation")
                away_team_abbr = game_data.get("visitor_team", {}).get("abbreviation")
                home_score = game_data.get("home_team_score")
                away_score = game_data.get("visitor_team_score")

                existing_game = session.query(NFLGame).filter(NFLGame.id == game_id).first()
                if existing_game:
                    continue

                new_game = NFLGame(
                    id=game_id,
                    season=SEASON,
                    date=game_date,
                    home_team_abbr=home_team_abbr,
                    away_team_abbr=away_team_abbr,
                    home_score=home_score,
                    away_score=away_score
                )
                session.add(new_game)

                derived_record = NFLGameDerived(
                    game_id=game_id,
                    processed=False
                )
                session.add(derived_record)

                added_count += 1

            session.commit()
            api_cursor = games_page.meta.next_cursor
            if not api_cursor:
                break

        print(f"Finished populating NFL games for season {SEASON}.")
        print(f"Total new games added: {added_count}")
        print(f"Skipped {skipped_count} non-final or postseason games.")

    except Exception as e:
        session.rollback()
        print(f"Error populating NFL games: {e}")
        raise
    finally:
        close_session(session)


if __name__ == "__main__":
    populate_all_nfl_games()