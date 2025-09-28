from database_config import get_db_session, close_session
from models import NFLTeam, NFLGameDerived

def reset_NFL_stats():
    session = get_db_session()
    try:
        print("Resetting team stats...")
        session.query(NFLTeam).update({
            NFLTeam.wins: 0,
            NFLTeam.losses: 0,
            NFLTeam.win_percentage: 0.0,
            NFLTeam.points_for: 0.0,
            NFLTeam.points_against: 0.0,
            NFLTeam.points_differential: 0.0,
            NFLTeam.catelo: 1000.0
        }, synchronize_session=False)
        
        print("Resetting processing status...")
        session.query(NFLGameDerived).update({
            NFLGameDerived.processed: False,
            NFLGameDerived.home_pre_catelo: None,
            NFLGameDerived.away_pre_catelo: None,
            NFLGameDerived.home_post_catelo: None,
            NFLGameDerived.away_post_catelo: None
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
    reset_NFL_stats()