import os
import requests

# Directory to save logos
os.makedirs("logos", exist_ok=True)

# NFL team abbreviations (as used by NFL.com)
teams = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LV", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WAS"
]

base_url = "https://static.www.nfl.com/league/api/clubs/logos"

for code in teams:
    logo_url = f"{base_url}/{code}.svg"
    filename = f"logos/{code}.svg"
    try:
        response = requests.get(logo_url)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Saved {code}.svg")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {code}: {e}")


        