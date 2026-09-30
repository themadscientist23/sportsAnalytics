# Sports Analytics Platform

Custom Elo ("CatElo") ratings for NBA, NFL, and MLB. FastAPI + MySQL backend, React frontend. Work in progress.

## Before catelo stuff

- [ ] rebuild the mysql tables for the new schema. nothing in the repo makes tables yet, so write a `scripts/create_tables.py`
- [ ] backfill every sport, run `python -m sports.process_games <sport>`, make sure standings + team pages actually work
- [ ] fix the crontab path -> `backend/scripts/run_daily.zsh`
- [ ] clean up the frontend: one api base url instead of `127.0.0.1:8000` everywhere, a season picker (always shows latest rn), kill unused imports
- [ ] current season lives in two places (config `current_season` vs latest season in the db). pick one
- [ ] `with SessionLocal()` vs `try/finally` + `close_session`?
- [ ] tests?

## Then

- actually tune catelo per sport (still a placeholder)


## How to run locally

Backend:
```
cd backend
cp .env.example .env 
source venv/bin/activate
uvicorn main:app --reload
```

Frontend:
```
cd frontend
npm install
npm run dev
```


*Runs at http://localhost:5173*
