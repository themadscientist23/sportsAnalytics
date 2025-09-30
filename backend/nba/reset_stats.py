from database_config import get_db_session, close_session
from models import NBATeam, NBAGameDerived

def reset_nba_stats():
    session = get_db_session()
    try:
        print("Resetting team stats...")
        session.query(NBATeam).update({
            NBATeam.wins: 0,
            NBATeam.losses: 0,
            NBATeam.points_for: 0.0,
            NBATeam.points_against: 0.0,
            NBATeam.catelo: 1000.0
        }, synchronize_session=False)
        
        print("Resetting processing status...")
        session.query(NBAGameDerived).update({
            NBAGameDerived.processed: False,
            NBAGameDerived.home_pre_catelo: None,
            NBAGameDerived.away_pre_catelo: None,
            NBAGameDerived.home_post_catelo: None,
            NBAGameDerived.away_post_catelo: None
        }, synchronize_session=False)
        
        session.commit()
        print("Reset Complete")

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        raise
    finally:
        close_session(session)


if __name__ == "__main__":
    reset_nba_stats()