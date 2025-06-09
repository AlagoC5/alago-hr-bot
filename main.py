from statcast_fetcher import fetch_stats as fetch_statcast_data
from scraper_dk import scrape_dk
from scraper_fd import scrape_fd
from sheet_output import update_google_sheet
from discord_poster import post_to_discord

def main():
    print("🚀 Running Alago HR AI Model...")

    # Step 1: Scrape DraftKings
    print("🟢 Scraping DraftKings...")
    dk_data = scrape_dk()

    # Step 2: Scrape FanDuel
    print("🔵 Scraping FanDuel...")
    fd_data = scrape_fd()

    # Step 3: Fetch Statcast stats
    print("📈 Fetching Statcast data...")
    statcast_data = fetch_statcast_data()

    # Step 4: Merge and analyze data
    print("🧠 Combining data for predictions...")
    combined = {}

    for player in set(dk_data.keys()).union(fd_data.keys()):
        odds_data = dk_data.get(player) or fd_data.get(player)
        stats = statcast_data.get(player)

        if not odds_data or not stats:
            continue

        implied_prob = odds_data["implied_prob"]
        odds = odds_data["odds"]
        source = odds_data["book"]

        true_prob = stats["HR/PA"]
        ev = round((true_prob * odds) - (1 - true_prob), 3)

        combined[player] = {
            "Team": odds_data["team"],
            "Odds": odds,
            "Book": source,
            "HR%": round(true_prob * 100, 1),
            "Barrel%": stats["barrel%"],
            "Implied%": round(implied_prob * 100, 1),
            "EV": ev,
        }

    if not combined:
        print("❌ No matches found between props and Statcast stats.")
        return

    # Step 5: Sort by EV and update sheet
    sorted_data = dict(sorted(combined.items(), key=lambda x: x[1]["EV"], reverse=True))
    update_google_sheet(sorted_data)

    # Step 6: Post top 5 to Discord
    post_to_discord(sorted_data)

    print("✅ Done.")

if __name__ == "__main__":
    main()
