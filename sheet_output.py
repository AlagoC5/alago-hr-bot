import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

def push_to_sheet(predictions):
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name('gcreds.json', [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ])
        client = gspread.authorize(creds)

        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        sheet = client.open_by_key(sheet_id).sheet1

        # Clear existing data
        sheet.clear()

        # Add headers
        sheet.append_row([
            "Player", "Team", "Opponent", "Odds",
            "True HR Probability", "Expected Value", "AI Rating"
        ])

        # Add each prediction row
        for p in predictions:
            sheet.append_row([
                p['player'],
                p['team'],
                p['opponent'],
                p['odds'],
                p['true_prob'],
                p['ev'],
                p['ai_rating']
            ])
        print("✅ Google Sheet updated.")
    except Exception as e:
        print(f"❌ Failed to update sheet: {e}")
