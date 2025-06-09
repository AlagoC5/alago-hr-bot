import os
from dotenv import load_dotenv
load_dotenv()

from scraper_dk import scrape_dk
from scraper_fd import scrape_fd
from statcast_fetcher import fetch_stats
from model_engine import run_model
from sheet_output import push_to_sheet
from discord_poster import post_to_discord, send_alert

def main():
    print("🟢 Scraping DraftKings...")
    dk_data = scrape_dk()

    print("🟦 Scraping FanDuel...")
    fd_data = scrape_fd()

    # ✅ Alert if any props are live
    total_props = len(dk_data) + len(fd_data)
    if total_props > 0:
        send_alert(f"🚨 Home Run Props Are LIVE!\nDK: {len(dk_data)} | FD: {len(fd_data)}")

    print("📊 Fetching Statcast stats...")
    stats = fetch_stats()

    print("🧠 Running prediction model...")
    all_props = dk_data + fd_data
    predictions = run_model(all_props, stats)

    print("📤 Updating Google Sheet...")
    push_to_sheet(predictions)

    print("📬 Posting to Discord...")
    post_to_discord(predictions)

if __name__ == "__main__":
    main()
