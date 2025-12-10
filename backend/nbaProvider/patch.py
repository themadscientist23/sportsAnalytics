import time, sys, os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_config import get_db_session, close_session, api
from models import NBAGame, NBAGameDerived

API_KEY = "7c8468fa-393e-49cc-92c2-bf25160a6f8c"
SEASON = 2025
PATCH_DATE = "2025-09-01"
PATCH_END_DATE = "2025-11-21"

session = get_db_session()

try:
    # Fetch games for the patch date
    games_page = api.nba.games.list(
        seasons=[SEASON],
        per_page=100,
        start_date=PATCH_DATE,
        end_date=PATCH_END_DATE
    )

    for g in games_page.data:
        time.sleep(60)
        game = g.model_dump()
        if game.get("status") != "Final" or game.get("postseason"):
            continue

        game_id = game.get("id")
        game_date = datetime.strptime(game.get("date"), "%Y-%m-%d").date()
        home_team_abbr = game.get("home_team", {}).get("abbreviation")
        away_team_abbr = game.get("visitor_team", {}).get("abbreviation")
        home_score = game.get("home_team_score")
        away_score = game.get("visitor_team_score")

        # Check if game already exists
        existing_game = session.query(NBAGame).filter(NBAGame.gid == game_id).first()
        if existing_game:
            print(f"Game {game_id} already exists, skipping...")
            continue
        

        # Create new game
        new_game = NBAGame(
            gid=game_id,
            season=SEASON,
            date=game_date,
            home_team_abbr=home_team_abbr,
            away_team_abbr=away_team_abbr,
            home_score=home_score,
            away_score=away_score
        )
        print(f"Adding game {game_id} on {game_date}: {home_team_abbr} vs {away_team_abbr}")
        
        session.add(new_game)
        
        derived_record = NBAGameDerived(
            game_gid=game_id,
            processed=False
        )
        session.add(derived_record)
        
        print(f"Inserted {PATCH_DATE}: {home_team_abbr} {home_score} - {away_team_abbr} {away_score}")

    session.commit()
    print(f"Patch complete for {PATCH_DATE} to {PATCH_END_DATE}.")
    
except Exception as e:
    session.rollback()
    print(f"Error patching NBA games: {e}")
    raise
finally:
    close_session(session)