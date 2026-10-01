"""initial schema"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '9295a99d5e05'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('mlb_teams',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('abbreviation', sa.String(length=10), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mlb_teams_abbreviation'), 'mlb_teams', ['abbreviation'], unique=False)
    op.create_table('nba_teams',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('abbreviation', sa.String(length=10), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nba_teams_abbreviation'), 'nba_teams', ['abbreviation'], unique=False)
    op.create_table('nfl_teams',
    sa.Column('home_adv', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('abbreviation', sa.String(length=10), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nfl_teams_abbreviation'), 'nfl_teams', ['abbreviation'], unique=False)
    op.create_table('mlb_games',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('season', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('postseason', sa.Boolean(), nullable=False),
    sa.Column('home_score', sa.Integer(), nullable=False),
    sa.Column('away_score', sa.Integer(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['mlb_teams.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['mlb_teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mlb_games_date'), 'mlb_games', ['date'], unique=False)
    op.create_index('ix_mlb_games_season_away', 'mlb_games', ['season', 'away_team_id'], unique=False)
    op.create_index('ix_mlb_games_season_home', 'mlb_games', ['season', 'home_team_id'], unique=False)
    op.create_table('nba_games',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('season', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('postseason', sa.Boolean(), nullable=False),
    sa.Column('home_score', sa.Integer(), nullable=False),
    sa.Column('away_score', sa.Integer(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['nba_teams.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['nba_teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nba_games_date'), 'nba_games', ['date'], unique=False)
    op.create_index('ix_nba_games_season_away', 'nba_games', ['season', 'away_team_id'], unique=False)
    op.create_index('ix_nba_games_season_home', 'nba_games', ['season', 'home_team_id'], unique=False)
    op.create_table('nfl_games',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('season', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('postseason', sa.Boolean(), nullable=False),
    sa.Column('home_score', sa.Integer(), nullable=False),
    sa.Column('away_score', sa.Integer(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['nfl_teams.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['nfl_teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nfl_games_date'), 'nfl_games', ['date'], unique=False)
    op.create_index('ix_nfl_games_season_away', 'nfl_games', ['season', 'away_team_id'], unique=False)
    op.create_index('ix_nfl_games_season_home', 'nfl_games', ['season', 'home_team_id'], unique=False)
    op.create_table('mlb_game_ratings',
    sa.Column('home_pre_catelo', sa.Float(), nullable=False),
    sa.Column('away_pre_catelo', sa.Float(), nullable=False),
    sa.Column('home_post_catelo', sa.Float(), nullable=False),
    sa.Column('away_post_catelo', sa.Float(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['mlb_games.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('game_id')
    )
    op.create_table('nba_game_ratings',
    sa.Column('home_pre_catelo', sa.Float(), nullable=False),
    sa.Column('away_pre_catelo', sa.Float(), nullable=False),
    sa.Column('home_post_catelo', sa.Float(), nullable=False),
    sa.Column('away_post_catelo', sa.Float(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['nba_games.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('game_id')
    )
    op.create_table('nfl_game_ratings',
    sa.Column('home_pre_catelo', sa.Float(), nullable=False),
    sa.Column('away_pre_catelo', sa.Float(), nullable=False),
    sa.Column('home_post_catelo', sa.Float(), nullable=False),
    sa.Column('away_post_catelo', sa.Float(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['nfl_games.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('game_id')
    )


def downgrade() -> None:
    op.drop_table('nfl_game_ratings')
    op.drop_table('nba_game_ratings')
    op.drop_table('mlb_game_ratings')
    op.drop_index('ix_nfl_games_season_home', table_name='nfl_games')
    op.drop_index('ix_nfl_games_season_away', table_name='nfl_games')
    op.drop_index(op.f('ix_nfl_games_date'), table_name='nfl_games')
    op.drop_table('nfl_games')
    op.drop_index('ix_nba_games_season_home', table_name='nba_games')
    op.drop_index('ix_nba_games_season_away', table_name='nba_games')
    op.drop_index(op.f('ix_nba_games_date'), table_name='nba_games')
    op.drop_table('nba_games')
    op.drop_index('ix_mlb_games_season_home', table_name='mlb_games')
    op.drop_index('ix_mlb_games_season_away', table_name='mlb_games')
    op.drop_index(op.f('ix_mlb_games_date'), table_name='mlb_games')
    op.drop_table('mlb_games')
    op.drop_index(op.f('ix_nfl_teams_abbreviation'), table_name='nfl_teams')
    op.drop_table('nfl_teams')
    op.drop_index(op.f('ix_nba_teams_abbreviation'), table_name='nba_teams')
    op.drop_table('nba_teams')
    op.drop_index(op.f('ix_mlb_teams_abbreviation'), table_name='mlb_teams')
    op.drop_table('mlb_teams')
