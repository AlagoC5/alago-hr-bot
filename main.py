from scraper_dk import scrape_dk
from scraper_fd import scrape_fd
from statcast_fetcher import fetch_statcast_data
from model_engine import run_prediction_model
from sheet_output import update_google_sheet
from discord_poster import post_to_discord

from datetime import datetime, timedelta

def run_model():
    print("🟢 Scraping DraftKings...")
    dk_data = scrape_dk()

    print("🟦 Scraping FanDuel...")
    fd_data = scrape_fd()

    all_props = dk_data + fd_data
    print(f"📦 Scraped {len(all_props)} total props:")

    for prop in all_props:
        print(f" - {prop['player_name']} @ {prop['odds']}")

    print("📊 Fetching Statcast stats...")
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    print(f"📊 Loading Statcast data from {start_date} to {end_date}...")

    statcast_stats = fetch_statcast_data(start_date, end_date)
    print(f"✅ Loaded stats for {len(statcast_stats)} players.")

    print("🧠 Running prediction model...")
    final_predictions = run_prediction_model(all_props, statcast_stats)

    print(f"🎯 Final Predictions: {len(final_predictions)} players selected")

    print("📤 Updating Google Sheet...")
    update_google_sheet(final_predictions)

    print("📬 Posting to Discord...")
    post_to_discord(final_predictions)

if __name__ == "__main__":
    run_model()
