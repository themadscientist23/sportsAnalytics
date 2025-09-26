from balldontlie import BalldontlieAPI
import mysql.connector
from datetime import datetime

API_KEY = "7c8468fa-393e-49cc-92c2-bf25160a6f8c"
SEASON = 2024
PATCH_DATE = "2024-12-01"

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="sportsdb"
)
cursor = conn.cursor()
api = BalldontlieAPI(api_key=API_KEY)

# Fetch games for April 8
games_page = api.nba.games.list(
    seasons=[SEASON],
    per_page=25,
    start_date=PATCH_DATE,
    end_date=PATCH_DATE
)

for g in games_page.data:
    game = g.model_dump()
    if game.get("status") != "Final" or game.get("postseason"):
        continue

    game_id = game.get("id")
    game_date = datetime.strptime(game.get("date"), "%Y-%m-%d").date()
    home_team = game.get("home_team", {}).get("abbreviation")
    away_team = game.get("visitor_team", {}).get("abbreviation")
    home_score = game.get("home_team_score")
    away_score = game.get("visitor_team_score")

    sql = """
        INSERT IGNORE INTO nba_games
        (id, season, date, home_team, home_score, away_team, away_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (game_id, SEASON, game_date, home_team, home_score, away_team, away_score)
    cursor.execute(sql, values)
    print(f"Inserted {PATCH_DATE}: {home_team} {home_score} - {away_team} {away_score}")

conn.commit()
cursor.close()
conn.close()
print(f"Patch complete for {PATCH_DATE}.")