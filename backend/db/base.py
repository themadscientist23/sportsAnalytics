from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import backref, declarative_base, declared_attr, relationship

Base = declarative_base()


class TeamBase:
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class GameBase:
    id = Column(Integer, primary_key=True, autoincrement=False)
    season = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, index=True)
    postseason = Column(Boolean, nullable=False, default=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)

    @declared_attr
    def home_team_id(cls):
        return Column(Integer, ForeignKey(f"{cls.__team_table__}.id"), nullable=False)

    @declared_attr
    def away_team_id(cls):
        return Column(Integer, ForeignKey(f"{cls.__team_table__}.id"), nullable=False)

    @declared_attr
    def home_team(cls):
        return relationship(cls.__team_class__, foreign_keys=f"{cls.__name__}.home_team_id")

    @declared_attr
    def away_team(cls):
        return relationship(cls.__team_class__, foreign_keys=f"{cls.__name__}.away_team_id")

    @declared_attr
    def __table_args__(cls):
        return (
            Index(f"ix_{cls.__tablename__}_season_home", "season", "home_team_id"),
            Index(f"ix_{cls.__tablename__}_season_away", "season", "away_team_id"),
        )


class GameRatingBase:
    home_pre_catelo = Column(Float, nullable=False)
    away_pre_catelo = Column(Float, nullable=False)
    home_post_catelo = Column(Float, nullable=False)
    away_post_catelo = Column(Float, nullable=False)

    @declared_attr
    def game_id(cls):
        return Column(
            Integer,
            ForeignKey(f"{cls.__game_table__}.id", ondelete="CASCADE"),
            primary_key=True,
        )

    @declared_attr
    def game(cls):
        return relationship(
            cls.__game_class__,
            backref=backref("rating", uselist=False, passive_deletes=True),
        )
