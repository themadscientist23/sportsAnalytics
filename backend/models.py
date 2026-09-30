from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, declared_attr
from datetime import datetime, timezone

Base = declarative_base()


class TeamBase:

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False, unique=True)

    # Basic record
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)

    # Calculated metrics
    points_for = Column(Float, default=0.0)
    points_against = Column(Float, default=0.0)
    catelo = Column(Float, default=1000.0)

    # Metadata
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class GameBase:
    __autoincrement_id__ = False

    season = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, index=True)

    home_score = Column(Integer)
    away_score = Column(Integer)

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=cls.__autoincrement_id__)

    @declared_attr
    def home_team_abbr(cls):
        return Column(String(10), ForeignKey(f'{cls.__team_table__}.abbreviation'), nullable=False)

    @declared_attr
    def away_team_abbr(cls):
        return Column(String(10), ForeignKey(f'{cls.__team_table__}.abbreviation'), nullable=False)

    @declared_attr
    def home_team(cls):
        return relationship(cls.__team_class__, foreign_keys=f"{cls.__name__}.home_team_abbr")

    @declared_attr
    def away_team(cls):
        return relationship(cls.__team_class__, foreign_keys=f"{cls.__name__}.away_team_abbr")


class GameDerivedBase:
    processed = Column(Boolean, default=False)

    home_pre_catelo = Column(Float)
    away_pre_catelo = Column(Float)

    home_post_catelo = Column(Float)
    away_post_catelo = Column(Float)

    @declared_attr
    def game_id(cls):
        return Column(
            Integer,
            ForeignKey(f'{cls.__game_table__}.id', ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
            unique=True,
        )

    @declared_attr
    def game(cls):
        return relationship(
            cls.__game_class__,
            backref="derived_row",
            passive_deletes=True,
            uselist=False,
        )


class NBATeam(TeamBase, Base):
    __tablename__ = 'nba_teams'


class MLBTeam(TeamBase, Base):
    __tablename__ = 'mlb_teams'


class NFLTeam(TeamBase, Base):
    __tablename__ = 'nfl_teams'

    ties = Column(Integer, default=0)
    home_adv = Column(Float, default=100.0)


class NBAGame(GameBase, Base):
    __tablename__ = 'nba_games'
    __team_class__ = "NBATeam"
    __team_table__ = "nba_teams"
    __autoincrement_id__ = False


class MLBGame(GameBase, Base):
    __tablename__ = 'mlb_games'
    __team_class__ = "MLBTeam"
    __team_table__ = "mlb_teams"
    __autoincrement_id__ = False


class NFLGame(GameBase, Base):
    __tablename__ = 'nfl_games'
    __team_class__ = "NFLTeam"
    __team_table__ = "nfl_teams"
    __autoincrement_id__ = False


class NBAGameDerived(GameDerivedBase, Base):
    __tablename__ = "nba_games_derived"
    __game_class__ = "NBAGame"
    __game_table__ = "nba_games"


class MLBGameDerived(GameDerivedBase, Base):
    __tablename__ = 'mlb_games_derived'
    __game_class__ = "MLBGame"
    __game_table__ = "mlb_games"


class NFLGameDerived(GameDerivedBase, Base):
    __tablename__ = 'nfl_games_derived'
    __game_class__ = "NFLGame"
    __game_table__ = "nfl_games"
