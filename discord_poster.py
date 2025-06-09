import os
import requests

def post_to_discord(predictions):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("❌ No webhook URL found in .env")
        return

    if not predictions:
        print("⚠️ No predictions to post.")
        return

    message = "**🔥 AlagoBets Home Run AI Picks Today:**\\n\\n"
    for p in predictions:
        message += f"**{p['player']}** ({p['team']}) vs {p['opponent']}\\n"
        message += f"Odds: +{p['odds']} | EV: {p['ev']} | AI Score: {p['ai_rating']}\\n\\n"

    response = requests.post(webhook_url, json={"content": message})
    if response.status_code == 204:
        print("✅ Picks posted to Discord successfully.")
    else:
        print(f"❌ Discord error: {response.status_code} - {response.text}")
def send_alert(message):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ No webhook URL set.")
        return
    requests.post(webhook_url, json={"content": message})
