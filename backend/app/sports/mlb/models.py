from app.db.base import Base, GameBase, GameRatingBase, TeamBase


class MLBTeam(TeamBase, Base):
    __tablename__ = "mlb_teams"


class MLBGame(GameBase, Base):
    __tablename__ = "mlb_games"
    __team_class__ = "MLBTeam"
    __team_table__ = "mlb_teams"


class MLBGameRating(GameRatingBase, Base):
    __tablename__ = "mlb_game_ratings"
    __game_class__ = "MLBGame"
    __game_table__ = "mlb_games"
