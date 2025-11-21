from sqlalchemy.orm import joinedload
from database_config import get_db_session, close_session
from models import MLBGame, MLBGameDerived, MLBTeam


def calculate_catelo(home_team, away_team, game_date, home_score, away_score):
    """
    Calculate CatElo rating changes based on Elo algorithm with margin of victory.
    
    Uses standard Elo formula:
    - Expected win probability based on rating difference
    - K-factor of 20 (standard for sports)
    - Margin of victory multiplier (bigger wins = bigger changes)
    - Home advantage of ~50 points (baseball has less home advantage than basketball)
    """
    import math
    
    # Constants
    K_FACTOR = 20  # Base K-factor
    HOME_ADVANTAGE = 50  # Home team gets ~50 rating points advantage
    
    # Get pre-game ratings
    home_rating = home_team.catelo
    away_rating = away_team.catelo
    
    # Adjust for home advantage
    adjusted_home_rating = home_rating + HOME_ADVANTAGE
    
    # Calculate expected win probability for home team
    rating_diff = adjusted_home_rating - away_rating
    expected_home_win = 1 / (1 + 10 ** (-rating_diff / 400))
    
    # Determine actual result (1 if home wins, 0 if away wins)
    if home_score > away_score:
        actual_result = 1
        margin = home_score - away_score
    elif away_score > home_score:
        actual_result = 0
        margin = away_score - home_score
    else:
        # Tie - both teams get small adjustment
        actual_result = 0.5
        margin = 0
    
    # Margin of victory multiplier (logarithmic scale)
    # Bigger wins matter more, but with diminishing returns
    if margin > 0:
        mov_multiplier = math.log(max(margin, 1) + 1) / math.log(2)  # log2(margin + 1)
        mov_multiplier = min(mov_multiplier, 2.0)  # Cap at 2x
    else:
        mov_multiplier = 1.0
    
    # Calculate rating change
    rating_change = K_FACTOR * mov_multiplier * (actual_result - expected_home_win)
    
    # Apply changes
    home_team.catelo += rating_change
    away_team.catelo -= rating_change


def process_MLB_games():
    session = get_db_session()
    try:
        unprocessed_rows = (
            session.query(MLBGameDerived)
            .options(joinedload(MLBGameDerived.game))
            .filter(MLBGameDerived.processed == False)
            .join(MLBGame)
            .order_by(MLBGame.date)
            .all()
        )

        if not unprocessed_rows:
            print("No unprocessed MLB games found")
            return

        print(f"Found {len(unprocessed_rows)} unprocessed games. Starting processing...")

        teams_cache = {team.abbreviation: team for team in session.query(MLBTeam).all()}

        for derived_row in unprocessed_rows:
            game = derived_row.game
            home_team = teams_cache[game.home_team_abbr]
            away_team = teams_cache[game.away_team_abbr]

            derived_row.home_pre_catelo = home_team.catelo
            derived_row.away_pre_catelo = away_team.catelo

            if game.home_score > game.away_score:
                home_team.wins += 1
                away_team.losses += 1
            else:
                away_team.wins += 1
                home_team.losses += 1

            # Apply Cat-Elo update
            calculate_catelo(home_team, away_team, game.date, game.home_score, game.away_score)

            home_team.points_for += game.home_score
            home_team.points_against += game.away_score
            away_team.points_for += game.away_score
            away_team.points_against += game.home_score

            derived_row.home_post_catelo = home_team.catelo
            derived_row.away_post_catelo = away_team.catelo

            derived_row.processed = True

            print(
                f"Processed: {game.date.strftime('%Y-%m-%d')} - "
                f"{away_team.abbreviation} ({game.away_score}) @ "
                f"{home_team.abbreviation} ({game.home_score})"
            )


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
    process_MLB_games()