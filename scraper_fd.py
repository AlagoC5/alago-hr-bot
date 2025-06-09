import requests
import re

def scrape_fd():
    url = "https://sportsbook.fanduel.com/navigation/mlb"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ FanDuel request failed.")
        return []

    html = response.text
    pattern = re.compile(r'"label":"To Hit a Home Run","outcomes":\[(.*?)\]')
    players = []

    for match in re.finditer(pattern, html):
        odds_block = match.group(1)
        entries = re.findall(r'"label":"(.*?)".*?"odds":(-?\d+)', odds_block)
        for name, odds in entries:
            players.append({
                "player": name.strip(),
                "book": "FanDuel",
                "odds": int(odds)
            })

    print(f"✅ FanDuel scraped {len(players)} props.")
    return players
