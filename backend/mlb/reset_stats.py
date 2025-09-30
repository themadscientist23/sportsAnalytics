from database_config import get_db_session, close_session
from models import MLBTeam, MLBGameDerived

def reset_MLB_stats():
    session = get_db_session()
    try:
        print("Resetting team stats...")
        session.query(MLBTeam).update({
            MLBTeam.wins: 0,
            MLBTeam.losses: 0,
            MLBTeam.points_for: 0.0,
            MLBTeam.points_against: 0.0,
            MLBTeam.catelo: 1000.0
        }, synchronize_session=False)
        
        print("Resetting processing status...")
        session.query(MLBGameDerived).update({
            MLBGameDerived.processed: False,
            MLBGameDerived.home_pre_catelo: None,
            MLBGameDerived.away_pre_catelo: None,
            MLBGameDerived.home_post_catelo: None,
            MLBGameDerived.away_post_catelo: None
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
    reset_MLB_stats()