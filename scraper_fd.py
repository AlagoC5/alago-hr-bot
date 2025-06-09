import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def scrape_fd():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get("https://sportsbook.fanduel.com/navigation/mlb")

    time.sleep(10)  # Let everything load

    props = []
    try:
        all_rows = driver.find_elements(By.CSS_SELECTOR, "div[class*='market']")

        for row in all_rows:
            try:
                label = row.find_element(By.CSS_SELECTOR, "div[class*='event-title']").text
                if "To Hit a Home Run" not in label:
                    continue

                names = row.find_elements(By.CSS_SELECTOR, "span[class*='outcome-name']")
                odds = row.find_elements(By.CSS_SELECTOR, "span[class*='outcome-odds']")

                for i in range(min(len(names), len(odds))):
                    player = names[i].text.strip()
                    odd = odds[i].text.strip().replace("+", "")
                    if player and odd.isnumeric():
                        props.append({
                            "player": player,
                            "odds": int(odd),
                            "team": "N/A",
                            "opponent": "N/A"
                        })

            except Exception:
                continue

    except Exception as e:
        print(f"❌ FD scrape error: {e}")

    driver.quit()
    return props
