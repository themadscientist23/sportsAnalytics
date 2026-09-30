from sqlalchemy import Column, Float

from db.base import Base, GameBase, GameRatingBase, TeamBase


class NFLTeam(TeamBase, Base):
    __tablename__ = "nfl_teams"

    home_adv = Column(Float, nullable=False, default=100.0)


class NFLGame(GameBase, Base):
    __tablename__ = "nfl_games"
    __team_class__ = "NFLTeam"
    __team_table__ = "nfl_teams"


class NFLGameRating(GameRatingBase, Base):
    __tablename__ = "nfl_game_ratings"
    __game_class__ = "NFLGame"
    __game_table__ = "nfl_games"
