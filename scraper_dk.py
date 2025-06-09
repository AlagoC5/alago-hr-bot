import requests
import re

def scrape_dk():
    url = "https://sportsbook.draftkings.com/leagues/baseball/mlb"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ DraftKings request failed.")
        return []

    html = response.text
    pattern = re.compile(r'"label":"(.*?)","outcomes":\[(.*?)\]')
    players = []

    for match in re.finditer(pattern, html):
        label = match.group(1)
        if "To Hit a Home Run" not in label:
            continue
        try:
            name = label.replace("To Hit a Home Run - ", "").strip()
            odds_data = match.group(2)
            odds_match = re.search(r'"odds":(-?\d+)', odds_data)
            if odds_match:
                odds = int(odds_match.group(1))
                players.append({
                    "player": name,
                    "book": "DraftKings",
                    "odds": odds
                })
        except Exception as e:
            continue

    print(f"✅ DraftKings scraped {len(players)} props.")
    return players
