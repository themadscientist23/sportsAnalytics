from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class NBATeam(Base):
    __tablename__ = 'nba_teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False, unique=True)
    
    # Basic record
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    
    # Calculated metrics
    win_percentage = Column(Float, default=0.0)
    points_for = Column(Float, default=0.0)
    points_against = Column(Float, default=0.0)
    points_differential = Column(Float, default=0.0)
    catelo = Column(Float, default=1000.0)
    
    # Metadata
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))   

class MLBTeam(Base):
    __tablename__ = 'mlb_teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False, unique=True)
    
    # Basic record
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    
    # Calculated metrics
    win_percentage = Column(Float, default=0.0)
    points_for = Column(Float, default=0.0)
    points_against = Column(Float, default=0.0)
    points_differential = Column(Float, default=0.0)
    catelo = Column(Float, default=1000.0)
    
    # Metadata
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class NFLTeam(Base):
    __tablename__ = 'nfl_teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False, unique=True)
    
    # Basic record
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ties = Column(Integer, default=0)
    
    # Calculated metrics
    win_percentage = Column(Float, default=0.0)
    points_for = Column(Float, default=0.0)
    points_against = Column(Float, default=0.0)
    points_differential = Column(Float, default=0.0)
    catelo = Column(Float, default=1000.0)
    
    # Metadata
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class NBAGame(Base):
    __tablename__ = 'nba_games'
    
    gid = Column(Integer, primary_key=True, autoincrement=False)
    season = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    # Team references
    home_team_abbr = Column(String(10), ForeignKey('nba_teams.abbreviation'), nullable=False)
    away_team_abbr = Column(String(10), ForeignKey('nba_teams.abbreviation'), nullable=False)
    
    # Scores
    home_score = Column(Integer)
    away_score = Column(Integer)
    
    # Relationships
    home_team = relationship("NBATeam", foreign_keys=[home_team_abbr])
    away_team = relationship("NBATeam", foreign_keys=[away_team_abbr])

class NBAGameOld(Base):
    __tablename__ = 'nba_games_old'
    
    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    # Team references
    home_team = Column(String(100))
    away_team = Column(String(100))

    # Scores
    home_score = Column(Integer)
    away_score = Column(Integer)
    

class NBAGameDerived(Base):
    __tablename__ = "nba_games_derived"

    game_gid = Column(
        Integer,
        ForeignKey("nba_games.gid", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        unique=True  
    )

    # Processing status
    processed = Column(Boolean, default=False)

    # Pre-game metrics
    home_pre_catelo = Column(Float)
    away_pre_catelo = Column(Float)

    # Post-game metrics
    home_post_catelo = Column(Float)
    away_post_catelo = Column(Float)

    # Relationship
    game = relationship(
        "NBAGame",
        backref="derived_row",
        passive_deletes=True,
        uselist=False
    )

class MLBGame(Base):
    __tablename__ = 'mlb_games'
    
    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    # Team references
    home_team_abbr = Column(String(10), ForeignKey('mlb_teams.abbreviation'), nullable=False)
    away_team_abbr = Column(String(10), ForeignKey('mlb_teams.abbreviation'), nullable=False)
    
    # Scores
    home_score = Column(Integer)
    away_score = Column(Integer)
    
    # Relationships
    home_team = relationship("MLBTeam", foreign_keys=[home_team_abbr])
    away_team = relationship("MLBTeam", foreign_keys=[away_team_abbr])

class MLBGameDerived(Base):
    __tablename__ = 'mlb_games_derived'
    
    game_id = Column(Integer, ForeignKey('mlb_games.id'), primary_key=True)
    
    # Processing status
    processed = Column(Boolean, default=False)
    
    # Pre-game metrics
    home_pre_catelo = Column(Float)
    away_pre_catelo = Column(Float)
    
    # Post-game metrics
    home_post_catelo = Column(Float)
    away_post_catelo = Column(Float)

class NFLGame(Base):
    __tablename__ = 'nfl_games'
    
    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    # Team references
    home_team_abbr = Column(String(10), ForeignKey('nfl_teams.abbreviation'), nullable=False)
    away_team_abbr = Column(String(10), ForeignKey('nfl_teams.abbreviation'), nullable=False)
    
    # Scores
    home_score = Column(Integer)
    away_score = Column(Integer)
    
    # Relationships
    home_team = relationship("NFLTeam", foreign_keys=[home_team_abbr])
    away_team = relationship("NFLTeam", foreign_keys=[away_team_abbr])

class NFLGameDerived(Base):
    __tablename__ = 'nfl_games_derived'
    
    game_id = Column(Integer, ForeignKey('nfl_games.id'), primary_key=True)
    
    # Processing status
    processed = Column(Boolean, default=False)
    
    # Pre-game metrics
    home_pre_catelo = Column(Float)
    away_pre_catelo = Column(Float)
    
    # Post-game metrics
    home_post_catelo = Column(Float)
    away_post_catelo = Column(Float)

