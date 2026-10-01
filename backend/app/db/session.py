from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    return SessionLocal()


def close_session(session):
    session.close()
