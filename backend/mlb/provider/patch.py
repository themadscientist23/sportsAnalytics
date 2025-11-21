from balldontlie import BalldontlieAPI
from datetime import datetime
from database_config import get_db_session, close_session, api
from models import MLBGame, MLBGameDerived

SEASON = 2025
PATCH_DATE = "2024-12-01"


# Get database session
session = get_db_session()

try:
    games_page = api.mlb.games.list(
        seasons=[SEASON],
        per_page=25,
        dates=[PATCH_DATE]
    )

    for g in games_page.data:
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
        existing_game = session.query(MLBGame).filter(MLBGame.id == game_id).first()
        if existing_game:
            print(f"Game {game_id} already exists, skipping...")
            continue

        # Create new game
        new_game = MLBGame(
            id=game_id,
            season=SEASON,
            date=game_date,
            home_team_abbr=home_team_abbr,
            away_team_abbr=away_team_abbr,
            home_score=home_score,
            away_score=away_score
        )
        
        session.add(new_game)
        
        # Create derived record for processing
        derived_record = MLBGameDerived(
            game_id=game_id,
            processed=False
        )
        session.add(derived_record)
        
        print(f"Inserted {PATCH_DATE}: {home_team_abbr} {home_score} - {away_team_abbr} {away_score}")

    session.commit()
    print(f"Patch complete for {PATCH_DATE}.")
    
except Exception as e:
    session.rollback()
    print(f"Error patching MLB games: {e}")
    raise
finally:
    close_session(session)