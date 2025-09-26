from balldontlie import BalldontlieAPI
import mysql.connector
import time
from datetime import datetime, timedelta

SEASON = 2024

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="sportsdb"
)
cursor = conn.cursor()


api = BalldontlieAPI(api_key="7c8468fa-393e-49cc-92c2-bf25160a6f8c")
api_cursor = None

def update_nba_games_daily():
    today = datetime.today().date()
    start_date = today - timedelta(days=2)
    end_date = today
    added_count = 0  # counter for inserted games

    while True:
        print("Fetching next page...")
        time.sleep(60)
        games_page = api.nba.games.list(
            seasons=[SEASON],
            per_page=100,
            cursor=api_cursor,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        page_games = games_page.data
        if not page_games:
            break

        for g in page_games:
            game_data = g.model_dump()
            if game_data.get("status") != "Final" or game_data.get("postseason"):
                continue

            game_id = game_data.get("id")
            game_date = datetime.strptime(game_data.get("date"), "%Y-%m-%d").date()
            home_team = game_data.get("home_team", {}).get("abbreviation")
            away_team = game_data.get("visitor_team", {}).get("abbreviation")
            home_score = game_data.get("home_team_score")
            away_score = game_data.get("visitor_team_score")

            sql = """
                INSERT IGNORE INTO nba_games
                (id, season, date, home_team, home_score, away_team, away_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (game_id, SEASON, game_date, home_team, home_score, away_team, away_score)
            cursor.execute(sql, values)
            # Count only if a new row was inserted
            if cursor.rowcount > 0:
                added_count += 1

        conn.commit()
        api_cursor = games_page.meta.next_cursor
        if not api_cursor:
            break

    print(f"Finished updating NBA games from {start_date} to {end_date}.")
    print(f"Total new games added: {added_count}")
    return added_count

if __name__ == "__main__":
    added = update_nba_games_daily()
    print(f"{datetime.now()}: Daily NBA update complete. {added} new games added.")
    cursor.close()
    conn.close()