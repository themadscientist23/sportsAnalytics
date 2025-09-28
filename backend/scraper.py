import os
import requests
from bs4 import BeautifulSoup
import time

# Folder to save logos
output_folder = "logos"
os.makedirs(output_folder, exist_ok=True)

# User-Agent header to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

# List of all 30 NBA team Wikipedia pages
team_pages = [
    "https://en.wikipedia.org/wiki/Boston_Celtics",
    "https://en.wikipedia.org/wiki/Los_Angeles_Lakers",
    "https://en.wikipedia.org/wiki/Chicago_Bulls",
    "https://en.wikipedia.org/wiki/Miami_Heat",
    "https://en.wikipedia.org/wiki/Golden_State_Warriors",
    "https://en.wikipedia.org/wiki/San_Antonio_Spurs",
    "https://en.wikipedia.org/wiki/New_York_Knicks",
    "https://en.wikipedia.org/wiki/Toronto_Raptors",
    "https://en.wikipedia.org/wiki/Philadelphia_76ers",
    "https://en.wikipedia.org/wiki/Milwaukee_Bucks",
    "https://en.wikipedia.org/wiki/Los_Angeles_Clippers",
    "https://en.wikipedia.org/wiki/Houston_Rockets",
    "https://en.wikipedia.org/wiki/Dallas_Mavericks",
    "https://en.wikipedia.org/wiki/Denver_Nuggets",
    "https://en.wikipedia.org/wiki/Phoenix_Suns",
    "https://en.wikipedia.org/wiki/Utah_Jazz",
    "https://en.wikipedia.org/wiki/Portland_Trail_Blazers",
    "https://en.wikipedia.org/wiki/Oklahoma_City_Thunder",
    "https://en.wikipedia.org/wiki/Orlando_Magic",
    "https://en.wikipedia.org/wiki/Indiana_Pacers",
    "https://en.wikipedia.org/wiki/Cleveland_Cavaliers",
    "https://en.wikipedia.org/wiki/Detroit_Pistons",
    "https://en.wikipedia.org/wiki/Memphis_Grizzlies",
    "https://en.wikipedia.org/wiki/New_Orleans_Pelicans",
    "https://en.wikipedia.org/wiki/Sacramento_Kings",
    "https://en.wikipedia.org/wiki/Washington_Wizards",
    "https://en.wikipedia.org/wiki/Charlotte_Hornets",
    "https://en.wikipedia.org/wiki/Atlanta_Hawks",
    "https://en.wikipedia.org/wiki/Minnesota_Timberwolves",
    "https://en.wikipedia.org/wiki/Brooklyn_Nets"
]

for team_url in team_pages:
    team_name = team_url.split('/')[-1].replace('_', ' ')
    print(f"\nProcessing team: {team_name}")
    
    try:
        # Fetch page
        print(f"Fetching page: {team_url}")
        response = requests.get(team_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page (status {response.status_code})")
            continue
        print("Page fetched successfully.")

        soup = BeautifulSoup(response.text, "html.parser")

        # Find the infobox table
        infobox = soup.find("table", class_="infobox vcard")
        if not infobox:
            print("No infobox vcard found.")
            continue
        print("Infobox found.")

        # Find the first <img> in the infobox
        images = infobox.find_all("img")
        if not images:
            print("No <img> found inside infobox.")
            continue
        elif len(images) < 2:
            print(f"Only one image found in infobox for {team_name}, using the first image.")
            logo_img = images[0]
        else:
            logo_img = images[1]
        print(f"Logo <img> found: {logo_img['src']}")

        # Build full URL and filename
        logo_url = "https:" + logo_img["src"]
        ext = os.path.splitext(logo_url)[1].split("?")[0]  # handle query params
        filename = f"{team_name.replace(' ', '_')}{ext}"
        filepath = os.path.join(output_folder, filename)

        # Download logo
        print(f"Downloading logo from {logo_url} to {filepath}...")
        r = requests.get(logo_url, headers=headers)
        if r.status_code != 200:
            print(f"Failed to download logo (status {r.status_code})")
            continue

        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"Downloaded successfully: {filename}")

        time.sleep(0.5)  # polite delay

    except Exception as e:
        print(f"Error processing {team_name}: {e}")

print("\nAll done!")