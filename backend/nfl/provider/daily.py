import time
from datetime import datetime, timedelta
from database_config import get_db_session, close_session, api
from backend.models import NFLGame, NFLGameDerived

SEASON = 2025
api_cursor = None

def update_nfl_games_daily():    
    global api_cursor
    session = get_db_session()
    
    try:
        today = datetime.today().date()
        start_date = today - timedelta(days=2)
        end_date = today
        added_count = 0

        while True:
            print("Next page...")
            time.sleep(60)
            games_page = api.nfl.games.list(
                seasons=[SEASON],
                per_page=100,
                cursor=api_cursor,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            page_games = games_page.data
            if not page_games:
                break

            for g in page_games:
                game_data = g.model_dump()
                if game_data.get("status") != "Final" or game_data.get("postseason"):
                    continue

                game_id = game_data.get("id")
                game_date = datetime.strptime(game_data.get("date"), "%Y-%m-%d").date()
                home_team_abbr = game_data.get("home_team", {}).get("abbreviation")
                away_team_abbr = game_data.get("visitor_team", {}).get("abbreviation")
                home_score = game_data.get("home_team_score")
                away_score = game_data.get("visitor_team_score")

                existing_game = session.query(NFLGame).filter(NFLGame.gid == game_id).first()
                if existing_game:
                    continue

                new_game = NFLGame(
                    gid=game_id,
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

        print(f"Finished updating NFL games from {start_date} to {end_date}.")
        print(f"Total new games added: {added_count}")
        return added_count
        
    except Exception as e:
        session.rollback()
        print(f"Error updating NFL games: {e}")
        raise
    finally:
        close_session(session)

if __name__ == "__main__":
    added = update_nfl_games_daily()
    print(f"{datetime.now()}: Daily NFL update complete. {added} new games added.")