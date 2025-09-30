from sqlalchemy.orm import joinedload
from database_config import get_db_session, close_session
from models import NBAGame, NBAGameDerived, NBATeam


def calculate_catelo(home_team, away_team, game_date, home_score, away_score):
    # Placeholder adjustments
    if home_score > away_score:
        home_team.catelo += 15
        away_team.catelo -= 15
    else:
        away_team.catelo += 15
        home_team.catelo -= 15


def process_nba_games():
    session = get_db_session()
    try:
        unprocessed_rows = (
            session.query(NBAGameDerived)
            .options(joinedload(NBAGameDerived.game))
            .filter(NBAGameDerived.processed == False)
            .join(NBAGame)
            .order_by(NBAGame.date)
            .all()
        )

        if not unprocessed_rows:
            print("No unprocessed NBA games found")
            return

        print(f"Found {len(unprocessed_rows)} unprocessed games. Starting processing...")

        teams_cache = {team.abbreviation: team for team in session.query(NBATeam).all()}

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
        print(f"Successfully processed and saved {len(unprocessed_rows)} games.")

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        session.rollback()
        raise
    finally:
        close_session(session)


if __name__ == "__main__":
    process_nba_games()