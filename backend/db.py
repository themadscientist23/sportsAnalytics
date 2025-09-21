import sqlite3


conn = sqlite3.connect('sports_analytics.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    win_percentage REAL DEFAULT 0.0,
    points_for INTEGER DEFAULT 0,
    points_against INTEGER DEFAULT 0,
    points_differential REAL DEFAULT 0.0
)
""")
å
teams_starting_data = [
    ("Lakers", 50, 32, 0.61, 8700, 8500, 200.0),
    ("Warriors", 48, 34, 0.59, 8600, 8400, 200.0),
    ("Celtics", 45, 37, 0.55, 8500, 8400, 100.0),
    ("Bulls", 40, 42, 0.49, 8300, 8400, -100.0),
    ("Heat", 42, 40, 0.51, 8400, 8380, 20.0)
]

if cursor.fetchone() is None:
    cursor.executemany(
        """
        INSERT OR IGNORE INTO teams (name, wins, losses, win_percentage, points_for, points_against, points_differential)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, teams_starting_data
    )


conn.commit()

def get_db():
    return conn, cursor
