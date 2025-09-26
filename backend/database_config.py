from balldontlie import BalldontlieAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



api = BalldontlieAPI(api_key="7c8468fa-393e-49cc-92c2-bf25160a6f8c")


def get_db_session():
    return sessionmaker(bind=create_engine("mysql+mysqlconnector://root:@localhost:3306/sportsdb"))()


def close_session(session):
    session.close()
