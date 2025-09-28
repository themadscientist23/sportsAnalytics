from sqlalchemy.orm import joinedload
from database_config import get_db_session, close_session
from models import NBAGame, NBAGameDerived, NBATeam


def process_nba_games():
    session = get_db_session()
    try:
        # Step 1: Find all unprocessed game rows, ordered by date
        # We use joinedload to efficiently fetch the related game and team data in one go.
        unprocessed_rows = session.query(NBAGameDerived).options(
            joinedload(NBAGameDerived.game)
        ).filter(NBAGameDerived.processed == False).join(NBAGame).order_by(NBAGame.date).all()

        if not unprocessed_rows:
            print("No unprocessed NBA games found. All up to date. ✅")
            return

        print(f"Found {len(unprocessed_rows)} unprocessed games. Starting processing...")

        # Step 2: Cache all teams in memory to avoid repeated database queries
        # This is much faster than fetching teams one by one inside the loop.
        teams_cache = {team.abbreviation: team for team in session.query(NBATeam).all()}

        # Step 3: Iterate through each game and process it
        for derived_row in unprocessed_rows:
            game = derived_row.game
            
            # Skip games with no score
            if game.home_score is None or game.away_score is None:
                continue

            home_team = teams_cache[game.home_team_abbr]
            away_team = teams_cache[game.away_team_abbr]

            # Store the Cat-Elo ratings *before* the game
            derived_row.home_pre_catelo = home_team.catelo
            derived_row.away_pre_catelo = away_team.catelo

            # Determine the winner and update records and Cat-Elo
            if game.home_score > game.away_score:
                # Home team wins
                home_team.wins += 1
                away_team.losses += 1
                home_team.catelo += 15
                away_team.catelo -= 15
            else:
                # Away team wins
                away_team.wins += 1
                home_team.losses += 1
                away_team.catelo += 15
                home_team.catelo -= 15
            
            # Update points for and against for both teams
            home_team.points_for += game.home_score
            home_team.points_against += game.away_score
            away_team.points_for += game.away_score
            away_team.points_against += game.home_score

            # Store the Cat-Elo ratings *after* the game
            derived_row.home_post_catelo = home_team.catelo
            derived_row.away_post_catelo = away_team.catelo
            
            # Mark this game as processed
            derived_row.processed = True
            
            print(f"Processed: {game.date.strftime('%Y-%m-%d')} - {away_team.abbreviation} ({game.away_score}) @ {home_team.abbreviation} ({game.home_score})")

        # Step 4: After processing all games, update calculated stats for all teams in the cache
        print("Updating team-level calculated stats (win %, point diff)...")
        for team in teams_cache.values():
            total_games = team.wins + team.losses
            if total_games > 0:
                team.win_percentage = round(team.wins / total_games, 4)
            
            team.points_differential = team.points_for - team.points_against

        # Step 5: Commit all changes to the database in a single transaction
        print("Committing all changes to the database...")
        session.commit()
        print(f"Successfully processed and saved {len(unprocessed_rows)} games. 🔥")

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        session.rollback()
        raise
    finally:
        close_session(session)


if __name__ == "__main__":
    process_nba_games()