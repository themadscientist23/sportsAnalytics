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

# List of all 30 NFL team Wikipedia pages
team_pages = [
  "https://en.wikipedia.org/wiki/Arizona_Cardinals",
  "https://en.wikipedia.org/wiki/Atlanta_Falcons",
  "https://en.wikipedia.org/wiki/Baltimore_Ravens",
  "https://en.wikipedia.org/wiki/Buffalo_Bills",
  "https://en.wikipedia.org/wiki/Carolina_Panthers",
  "https://en.wikipedia.org/wiki/Chicago_Bears",
  "https://en.wikipedia.org/wiki/Cincinnati_Bengals",
  "https://en.wikipedia.org/wiki/Cleveland_Browns",
  "https://en.wikipedia.org/wiki/Dallas_Cowboys",
  "https://en.wikipedia.org/wiki/Denver_Broncos",
  "https://en.wikipedia.org/wiki/Detroit_Lions",
  "https://en.wikipedia.org/wiki/Green_Bay_Packers",
  "https://en.wikipedia.org/wiki/Houston_Texans",
  "https://en.wikipedia.org/wiki/Indianapolis_Colts",
  "https://en.wikipedia.org/wiki/Jacksonville_Jaguars",
  "https://en.wikipedia.org/wiki/Kansas_City_Chiefs",
  "https://en.wikipedia.org/wiki/Las_Vegas_Raiders",
  "https://en.wikipedia.org/wiki/Los_Angeles_Chargers",
  "https://en.wikipedia.org/wiki/Los_Angeles_Rams",
  "https://en.wikipedia.org/wiki/Miami_Dolphins",
  "https://en.wikipedia.org/wiki/Minnesota_Vikings",
  "https://en.wikipedia.org/wiki/New_England_Patriots",
  "https://en.wikipedia.org/wiki/New_Orleans_Saints",
  "https://en.wikipedia.org/wiki/New_York_Giants",
  "https://en.wikipedia.org/wiki/New_York_Jets",
  "https://en.wikipedia.org/wiki/Philadelphia_Eagles",
  "https://en.wikipedia.org/wiki/Pittsburgh_Steelers",
  "https://en.wikipedia.org/wiki/San_Francisco_49ers",
  "https://en.wikipedia.org/wiki/Seattle_Seahawks",
  "https://en.wikipedia.org/wiki/Tampa_Bay_Buccaneers",
  "https://en.wikipedia.org/wiki/Tennessee_Titans",
  "https://en.wikipedia.org/wiki/Washington_Commanders"
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
        infobox = soup.find("table", class_="infobox")
        if not infobox:
            print("No infobox vcard found.")
            continue
        print("Infobox found.")

        # Find the first <img> in the infobox
        images = infobox.find_all("a")
        if not images:
            print("No <a> found inside infobox.")
            continue
        elif len(images) < 2:
            print(f"Only one image found in infobox for {team_name}, using the first image.")
            logo_img = images[0]
        else:
            logo_img = images[1]
        print(f"Logo <img> found: {logo_img['href']}")

        # Build full URL and filename
        logo_url = "https://en.wikipedia.org/" + logo_img["href"]
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
