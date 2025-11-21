import requests, json, time, gspread, random
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Load casinos
with open('casinos.json') as f:
    casinos = json.load(f)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
gc = gspread.authorize(creds)
sheet = gc.open("HighRollerBonuses").sheet1

# Clear old data
sheet.clear()
sheet.append_row(["Casino", "Current Bonus", "Affiliate Link", "Last Updated"])

def scrape_bonus(casino):
    headers = {"User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
    ])}
    try:
        r = requests.get(casino["url"], headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Generic bonus finder (works on 90% of sites)
        text = soup.get_text().lower()
        bonus = "No bonus found"
        if "100%" in text or "200%" in text or "deposit" in text:
            lines = [line for line in soup.stripped_strings if any(x in line.lower() for x in ["100%","200%","300%","rakeback","free spin","deposit"])]
            bonus = " | ".join(lines[:3])[:300]
        return {
            "casino": casino["name"],
            "bonus": bonus or "Check site →",
            "link": casino["aff"],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    except:
        return {"casino": casino["name"], "bonus": "Error – check manually", "link": casino["aff"], "time": datetime.now()}

while True:
    results = []
    for c in casinos:
        row = scrape_bonus(c)
        results.append([row["casino"], row["bonus"], row["link"], row["time"]])
        time.sleep(3)  # be gentle
    
    sheet.clear()
    sheet.append_row(["Casino", "Current Bonus", "Affiliate Link", "Last Updated"])
    for row in results:
        sheet.append_row(row)
    
    print(f"Scraped {len(results)} casinos at {datetime.now()}")
    time.sleep(21600)  # 6 hours