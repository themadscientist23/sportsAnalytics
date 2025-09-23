import sqlite3


conn = sqlite3.connect('sports_analytics.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS nfl_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    ties INTEGER DEFAULT 0,
    win_percentage REAL DEFAULT 0.0,
    points_for REAL DEFAULT 0.0,
    points_against REAL DEFAULT 0.0,
    points_differential REAL DEFAULT 0.0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mlb_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    win_percentage REAL DEFAULT 0.0,
    points_for REAL DEFAULT 0.0,
    points_against REAL DEFAULT 0.0,
    points_differential REAL DEFAULT 0.0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS nba_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    win_percentage REAL DEFAULT 0.0,
    points_for REAL DEFAULT 0.0,
    points_against REAL DEFAULT 0.0,
    points_differential REAL DEFAULT 0.0
)
""")

nfl_teams = [
    {"name":"Kansas City Chiefs","wins":15,"losses":2,"ties":0,"win_percentage":0.882,"points_for":22.6,"points_against":19.2,"points_differential":3.4},
    {"name":"Detroit Lions","wins":15,"losses":2,"ties":0,"win_percentage":0.882,"points_for":33.2,"points_against":20.1,"points_differential":13.1},
    {"name":"Philadelphia Eagles","wins":14,"losses":3,"ties":0,"win_percentage":0.824,"points_for":27.2,"points_against":17.8,"points_differential":9.4},
    {"name":"Minnesota Vikings","wins":14,"losses":3,"ties":0,"win_percentage":0.824,"points_for":25.4,"points_against":19.5,"points_differential":5.9},
    {"name":"Buffalo Bills","wins":13,"losses":4,"ties":0,"win_percentage":0.765,"points_for":30.9,"points_against":21.6,"points_differential":9.3},
    {"name":"Baltimore Ravens","wins":12,"losses":5,"ties":0,"win_percentage":0.706,"points_for":30.5,"points_against":21.2,"points_differential":9.3},
    {"name":"Washington Commanders","wins":12,"losses":5,"ties":0,"win_percentage":0.706,"points_for":28.5,"points_against":23.0,"points_differential":5.5},
    {"name":"Los Angeles Chargers","wins":11,"losses":6,"ties":0,"win_percentage":0.647,"points_for":23.6,"points_against":17.7,"points_differential":5.9},
    {"name":"Green Bay Packers","wins":11,"losses":6,"ties":0,"win_percentage":0.647,"points_for":27.1,"points_against":19.9,"points_differential":7.2},
    {"name":"Pittsburgh Steelers","wins":10,"losses":7,"ties":0,"win_percentage":0.588,"points_for":22.4,"points_against":20.4,"points_differential":2.0},
    {"name":"Houston Texans","wins":10,"losses":7,"ties":0,"win_percentage":0.588,"points_for":21.9,"points_against":21.9,"points_differential":0.0},
    {"name":"Denver Broncos","wins":10,"losses":7,"ties":0,"win_percentage":0.588,"points_for":25.0,"points_against":18.3,"points_differential":6.7},
    {"name":"Tampa Bay Buccaneers","wins":10,"losses":7,"ties":0,"win_percentage":0.588,"points_for":29.5,"points_against":22.6,"points_differential":6.9},
    {"name":"Los Angeles Rams","wins":10,"losses":7,"ties":0,"win_percentage":0.588,"points_for":21.6,"points_against":22.7,"points_differential":-1.1},
    {"name":"Seattle Seahawks","wins":10,"losses":7,"ties":0,"win_percentage":0.588,"points_for":22.1,"points_against":21.6,"points_differential":0.5},
    {"name":"Cincinnati Bengals","wins":9,"losses":8,"ties":0,"win_percentage":0.529,"points_for":27.8,"points_against":25.5,"points_differential":2.3},
    {"name":"Miami Dolphins","wins":8,"losses":9,"ties":0,"win_percentage":0.471,"points_for":20.3,"points_against":21.4,"points_differential":-1.1},
    {"name":"Indianapolis Colts","wins":8,"losses":9,"ties":0,"win_percentage":0.471,"points_for":22.2,"points_against":25.1,"points_differential":-2.9},
    {"name":"Atlanta Falcons","wins":8,"losses":9,"ties":0,"win_percentage":0.471,"points_for":22.9,"points_against":24.9,"points_differential":-2.0},
    {"name":"Arizona Cardinals","wins":8,"losses":9,"ties":0,"win_percentage":0.471,"points_for":23.5,"points_against":22.3,"points_differential":1.2},
    {"name":"Dallas Cowboys","wins":7,"losses":10,"ties":0,"win_percentage":0.412,"points_for":20.6,"points_against":27.5,"points_differential":-6.9},
    {"name":"New York Jets","wins":5,"losses":12,"ties":0,"win_percentage":0.294,"points_for":19.9,"points_against":23.8,"points_differential":-3.9},
    {"name":"Chicago Bears","wins":5,"losses":12,"ties":0,"win_percentage":0.294,"points_for":18.2,"points_against":21.8,"points_differential":-3.6},
    {"name":"Carolina Panthers","wins":5,"losses":12,"ties":0,"win_percentage":0.294,"points_for":20.1,"points_against":31.4,"points_differential":-11.3},
    {"name":"New Orleans Saints","wins":5,"losses":12,"ties":0,"win_percentage":0.294,"points_for":19.9,"points_against":23.4,"points_differential":-3.5},
    {"name":"San Francisco 49ers","wins":6,"losses":11,"ties":0,"win_percentage":0.353,"points_for":22.9,"points_against":25.6,"points_differential":-2.7},
    {"name":"New England Patriots","wins":4,"losses":13,"ties":0,"win_percentage":0.235,"points_for":17.0,"points_against":24.5,"points_differential":-7.5},
    {"name":"Las Vegas Raiders","wins":4,"losses":13,"ties":0,"win_percentage":0.235,"points_for":18.2,"points_against":25.5,"points_differential":-7.3},
    {"name":"Jacksonville Jaguars","wins":4,"losses":13,"ties":0,"win_percentage":0.235,"points_for":18.8,"points_against":25.6,"points_differential":-6.8},
    {"name":"Cleveland Browns","wins":3,"losses":14,"ties":0,"win_percentage":0.176,"points_for":15.2,"points_against":25.6,"points_differential":-10.4},
    {"name":"Tennessee Titans","wins":3,"losses":14,"ties":0,"win_percentage":0.176,"points_for":18.3,"points_against":27.1,"points_differential":-8.8},
    {"name":"New York Giants","wins":3,"losses":14,"ties":0,"win_percentage":0.176,"points_for":16.1,"points_against":24.4,"points_differential":-8.3}
]

mlb_teams = [
    {"name":"Los Angeles Dodgers","wins":98,"losses":64,"win_percentage":0.605,"points_for":5.2,"points_against":4.2,"points_differential":1.0},
    {"name":"Philadelphia Phillies","wins":95,"losses":67,"win_percentage":0.586,"points_for":4.8,"points_against":4.1,"points_differential":0.7},
    {"name":"New York Yankees","wins":94,"losses":68,"win_percentage":0.580,"points_for":5.0,"points_against":4.1,"points_differential":0.9},
    {"name":"Milwaukee Brewers","wins":93,"losses":69,"win_percentage":0.574,"points_for":4.8,"points_against":4.0,"points_differential":0.8},
    {"name":"San Diego Padres","wins":93,"losses":69,"win_percentage":0.574,"points_for":5.3,"points_against":4.1,"points_differential":1.2},
    {"name":"Cleveland Guardians","wins":92,"losses":69,"win_percentage":0.571,"points_for":4.4,"points_against":3.8,"points_differential":0.6},
    {"name":"Baltimore Orioles","wins":91,"losses":71,"win_percentage":0.562,"points_for":4.9,"points_against":4.3,"points_differential":0.6},
    {"name":"Atlanta Braves","wins":89,"losses":73,"win_percentage":0.549,"points_for":4.3,"points_against":3.7,"points_differential":0.6},
    {"name":"Arizona Diamondbacks","wins":89,"losses":73,"win_percentage":0.549,"points_for":5.5,"points_against":4.9,"points_differential":0.6},
    {"name":"Houston Astros","wins":88,"losses":73,"win_percentage":0.547,"points_for":4.6,"points_against":4.0,"points_differential":0.6},
    {"name":"Kansas City Royals","wins":86,"losses":76,"win_percentage":0.531,"points_for":4.5,"points_against":4.0,"points_differential":0.5},
    {"name":"Detroit Tigers","wins":86,"losses":76,"win_percentage":0.531,"points_for":4.6,"points_against":4.0,"points_differential":0.6},
    {"name":"Seattle Mariners","wins":85,"losses":77,"win_percentage":0.525,"points_for":4.2,"points_against":3.7,"points_differential":0.5},
    {"name":"St. Louis Cardinals","wins":83,"losses":79,"win_percentage":0.512,"points_for":4.4,"points_against":4.1,"points_differential":0.3},
    {"name":"Chicago Cubs","wins":83,"losses":79,"win_percentage":0.512,"points_for":4.5,"points_against":4.1,"points_differential":0.4},
    {"name":"Boston Red Sox","wins":81,"losses":81,"win_percentage":0.500,"points_for":4.6,"points_against":4.6,"points_differential":0.0},
    {"name":"Tampa Bay Rays","wins":80,"losses":82,"win_percentage":0.494,"points_for":4.1,"points_against":4.1,"points_differential":0.0},
    {"name":"Minnesota Twins","wins":80,"losses":82,"win_percentage":0.494,"points_for":4.6,"points_against":4.5,"points_differential":0.1},
    {"name":"San Francisco Giants","wins":80,"losses":82,"win_percentage":0.494,"points_for":4.3,"points_against":4.3,"points_differential":0.0},
    {"name":"Texas Rangers","wins":78,"losses":84,"win_percentage":0.481,"points_for":4.6,"points_against":4.6,"points_differential":0.0},
    {"name":"Cincinnati Reds","wins":77,"losses":85,"win_percentage":0.475,"points_for":4.3,"points_against":4.3,"points_differential":0.0},
    {"name":"Pittsburgh Pirates","wins":76,"losses":86,"win_percentage":0.469,"points_for":4.1,"points_against":4.6,"points_differential":-0.5},
    {"name":"Toronto Blue Jays","wins":74,"losses":88,"win_percentage":0.457,"points_for":4.1,"points_against":4.6,"points_differential":-0.5},
    {"name":"Washington Nationals","wins":71,"losses":91,"win_percentage":0.438,"points_for":4.1,"points_against":4.7,"points_differential":-0.6},
    {"name":"Oakland Athletics","wins":69,"losses":93,"win_percentage":0.426,"points_for":4.0,"points_against":4.7,"points_differential":-0.7},
    {"name":"Los Angeles Angels","wins":63,"losses":99,"win_percentage":0.389,"points_for":3.9,"points_against":4.9,"points_differential":-1.0},
    {"name":"Miami Marlins","wins":62,"losses":100,"win_percentage":0.383,"points_for":3.9,"points_against":5.2,"points_differential":-1.3},
    {"name":"Colorado Rockies","wins":61,"losses":101,"win_percentage":0.377,"points_for":4.2,"points_against":5.7,"points_differential":-1.5},
    {"name":"Chicago White Sox","wins":41,"losses":121,"win_percentage":0.253,"points_for":3.1,"points_against":5.0,"points_differential":-1.9},
    {"name":"New York Mets","wins":89,"losses":73,"win_percentage":0.549,"points_for":4.7,"points_against":4.3,"points_differential":0.4}
]


nba_teams = [
    {"name":"Oklahoma City Thunder","wins":68,"losses":14,"win_percentage":0.829,"points_for":120.5,"points_against":107.6,"points_differential":12.8},
    {"name":"Cleveland Cavaliers","wins":64,"losses":18,"win_percentage":0.780,"points_for":121.9,"points_against":112.4,"points_differential":9.5},
    {"name":"Boston Celtics","wins":63,"losses":19,"win_percentage":0.768,"points_for":116.3,"points_against":107.2,"points_differential":9.1},
    {"name":"Memphis Grizzlies","wins":58,"losses":24,"win_percentage":0.707,"points_for":121.7,"points_against":113.6,"points_differential":8.1},
    {"name":"Denver Nuggets","wins":56,"losses":26,"win_percentage":0.683,"points_for":120.8,"points_against":113.1,"points_differential":7.7},
    {"name":"New York Knicks","wins":54,"losses":28,"win_percentage":0.659,"points_for":116.1,"points_against":112.0,"points_differential":4.1},
    {"name":"Atlanta Hawks","wins":53,"losses":29,"win_percentage":0.646,"points_for":118.2,"points_against":111.2,"points_differential":7.0},
    {"name":"Minnesota Timberwolves","wins":51,"losses":31,"win_percentage":0.622,"points_for":115.4,"points_against":109.3,"points_differential":6.1},
    {"name":"Indiana Pacers","wins":50,"losses":32,"win_percentage":0.610,"points_for":114.3,"points_against":110.2,"points_differential":4.1},
    {"name":"LA Clippers","wins":49,"losses":33,"win_percentage":0.598,"points_for":108.2,"points_against":107.3,"points_differential":0.9},
    {"name":"Chicago Bulls","wins":47,"losses":35,"win_percentage":0.573,"points_for":110.5,"points_against":110.3,"points_differential":0.2},
    {"name":"Phoenix Suns","wins":46,"losses":36,"win_percentage":0.561,"points_for":111.0,"points_against":110.0,"points_differential":1.0},
    {"name":"Dallas Mavericks","wins":45,"losses":37,"win_percentage":0.549,"points_for":110.0,"points_against":110.5,"points_differential":-0.5},
    {"name":"Miami Heat","wins":44,"losses":38,"win_percentage":0.537,"points_for":110.0,"points_against":110.0,"points_differential":0.0},
    {"name":"Philadelphia 76ers","wins":43,"losses":39,"win_percentage":0.524,"points_for":109.0,"points_against":109.5,"points_differential":-0.5},
    {"name":"Sacramento Kings","wins":42,"losses":40,"win_percentage":0.512,"points_for":109.0,"points_against":109.0,"points_differential":0.0},
    {"name":"Toronto Raptors","wins":41,"losses":41,"win_percentage":0.500,"points_for":108.0,"points_against":108.0,"points_differential":0.0},
    {"name":"Brooklyn Nets","wins":40,"losses":42,"win_percentage":0.488,"points_for":107.0,"points_against":107.5,"points_differential":-0.5},
    {"name":"Detroit Pistons","wins":39,"losses":43,"win_percentage":0.476,"points_for":106.0,"points_against":107.0,"points_differential":-1.0},
    {"name":"Charlotte Hornets","wins":38,"losses":44,"win_percentage":0.463,"points_for":105.0,"points_against":106.0,"points_differential":-1.0},
    {"name":"Portland Trail Blazers","wins":37,"losses":45,"win_percentage":0.451,"points_for":104.0,"points_against":105.0,"points_differential":-1.0},
    {"name":"New Orleans Pelicans","wins":36,"losses":46,"win_percentage":0.439,"points_for":103.0,"points_against":104.0,"points_differential":-1.0},
    {"name":"San Antonio Spurs","wins":35,"losses":47,"win_percentage":0.427,"points_for":102.0,"points_against":103.0,"points_differential":-1.0},
    {"name":"Washington Wizards","wins":16,"losses":66,"win_percentage":0.195,"points_for":104.0,"points_against":115.0,"points_differential":-11.0},
    {"name":"Utah Jazz","wins":17,"losses":65,"win_percentage":0.207,"points_for":102.0,"points_against":121.2,"points_differential":-19.2},
    {"name":"Orlando Magic","wins":18,"losses":64,"win_percentage":0.220,"points_for":104.5,"points_against":116.0,"points_differential":-11.5},
    {"name":"Milwaukee Bucks","wins":42,"losses":40,"win_percentage":0.512,"points_for":113.0,"points_against":111.0,"points_differential":2.0},
    {"name":"Golden State Warriors","wins":48,"losses":34,"win_percentage":0.585,"points_for":118.0,"points_against":112.0,"points_differential":6.0},
    {"name":"Houston Rockets","wins":22,"losses":60,"win_percentage":0.268,"points_for":107.0,"points_against":114.0,"points_differential":-7.0},
    {"name":"Los Angeles Lakers","wins":50,"losses":32,"win_percentage":0.610,"points_for":113.4,"points_against":112.2,"points_differential":1.2}
]

# NFL insertion
cursor.execute("SELECT 1 FROM nfl_teams LIMIT 1")
if cursor.fetchone() is None:
    cursor.executemany(
        """
        INSERT OR IGNORE INTO nfl_teams
        (name, wins, losses, ties, win_percentage, points_for, points_against, points_differential)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(team["name"], team["wins"], team["losses"], team["ties"], team["win_percentage"],
          team["points_for"], team["points_against"], team["points_differential"])
         for team in nfl_teams]
    )

# MLB insertion
cursor.execute("SELECT 1 FROM mlb_teams LIMIT 1")
if cursor.fetchone() is None:
    cursor.executemany(
        """
        INSERT OR IGNORE INTO mlb_teams
        (name, wins, losses, win_percentage, points_for, points_against, points_differential)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [(team["name"], team["wins"], team["losses"], team["win_percentage"],
          team["points_for"], team["points_against"], team["points_differential"])
         for team in mlb_teams]
    )

# NBA insertion
cursor.execute("SELECT 1 FROM nba_teams LIMIT 1")
if cursor.fetchone() is None:
    cursor.executemany(
        """
        INSERT OR IGNORE INTO nba_teams
        (name, wins, losses, win_percentage, points_for, points_against, points_differential)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [(team["name"], team["wins"], team["losses"], team["win_percentage"],
          team["points_for"], team["points_against"], team["points_differential"])
         for team in nba_teams]
    )

conn.commit()


conn.commit()

def get_db():
    return conn, cursor
