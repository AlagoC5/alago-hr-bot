import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def scrape_dk():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=home-runs")

    time.sleep(10)  # wait for page to load

    props = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, 'div.event-cell__name-text')
        odds = driver.find_elements(By.CSS_SELECTOR, 'span.outcome-cell__line')

        for i in range(min(len(rows), len(odds))):
            name = rows[i].text.strip()
            odd_text = odds[i].text.strip().replace("+", "")
            if name and odd_text.isnumeric():
                props.append({
                    "player": name,
                    "odds": int(odd_text),
                    "team": "N/A",
                    "opponent": "N/A"
                })

    except Exception as e:
        print(f"❌ DK scrape error: {e}")

    driver.quit()
    return props
