# Sports Analytics Platform

Custom Elo ("CatElo") ratings for NBA, NFL, and MLB. FastAPI + MySQL backend, React frontend. Work in progress.

## Done

- fastAPI backend with endpoints for seasons, standings and team rating history
- mySQL via SQLAlchemy, with per-sport models (NBA, NFL, MLB) built on shared base classes
- game ingest from balldontlie: full-season backfill and a daily update
- rating pipeline per sport, reset each season
- react frontend with standings and team pages
- backend organized as an `app` package, with env settings in `core/` and dependency-injected DB sessions
- alembic migrations for the schema
- ruff linting and a pytest setup

## ToDo

- tag seasons to each game
- `pydantic-settings` for config?
- backfill and rate every sport
- frontend cleanup: one API base URL, a season picker, remove unused imports
- fix the daily cron path
- tune CatElo per sport (placeholder right now)
- more tests
