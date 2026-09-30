from db.base import Base, GameBase, GameRatingBase, TeamBase


class NBATeam(TeamBase, Base):
    __tablename__ = "nba_teams"


class NBAGame(GameBase, Base):
    __tablename__ = "nba_games"
    __team_class__ = "NBATeam"
    __team_table__ = "nba_teams"


class NBAGameRating(GameRatingBase, Base):
    __tablename__ = "nba_game_ratings"
    __game_class__ = "NBAGame"
    __game_table__ = "nba_games"
