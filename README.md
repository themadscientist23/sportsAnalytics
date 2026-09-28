# sportsAnalytics

Custom Elo ("CatElo") ratings for NBA, NFL, and MLB. FastAPI + MySQL backend, React frontend. Work in progress.

## Next steps

- Tune the CatElo formula (still a placeholder)
- Fix MLB logos (missing entirely; some abbreviations currently show the wrong sport's logo)
- Normalize `gid`/`id` primary key naming across sports
- Dedup per-sport pipeline code (NBA/NFL/MLB each duplicate `calculate_catelo`, provider scripts, and API routes) — once the Elo math settles, since the APIs return different field shapes per sport so it's not a trivial merge

## How to run locally

Backend:
```
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

Frontend:
```
cd frontend
npm install
npm run dev
```

Pull fresh data (all three sports):
```
cd backend
./run_daily.zsh
```
