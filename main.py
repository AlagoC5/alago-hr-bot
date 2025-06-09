from statcast_fetcher import fetch_stats
from scraper_dk import scrape_dk
from scraper_fd import scrape_fd
from sheet_output import post_to_google_sheet

def main():
    print("🔄 Starting MLB Home Run AI model...")

    # 1. Get Statcast stats
    stats = fetch_stats()

    # 2. Get odds data
    print("🟢 Scraping DraftKings...")
    dk_data = scrape_dk()

    print("🔵 Scraping FanDuel...")
    fd_data = scrape_fd()

    # 3. Combine props from both books
    all_props = dk_data + fd_data
    print(f"📦 Total props scraped: {len(all_props)}")

    # 4. Calculate EV and rating
    enriched_props = []
    for prop in all_props:
        name = prop["player"]
        if name not in stats:
            continue

        barrel = stats[name]["barrel%"]
        hr_pa = stats[name]["HR/PA"]
        odds = prop["odds_decimal"]
        implied_prob = 1 / odds

        ai_prob = hr_pa * (1 + barrel / 100)
        ev = round(ai_prob * odds - 1, 3)
        ai_rating = round(ai_prob * 100, 1)

        prop["barrel%"] = barrel
        prop["HR/PA"] = round(hr_pa, 3)
        prop["implied_prob"] = round(implied_prob, 3)
        prop["ai_prob"] = round(ai_prob, 3)
        prop["EV"] = ev
        prop["AI Rating"] = ai_rating

        enriched_props.append(prop)

    print(f"✅ Enriched props: {len(enriched_props)}")

    # 5. Filter for +EV and sort
    enriched_props.sort(key=lambda x: x["EV"], reverse=True)
    top_props = [p for p in enriched_props if p["EV"] > 0][:10]

    # 6. Send to Google Sheet
    post_to_google_sheet(top_props)
    print("📤 Posted to Google Sheet ✅")
