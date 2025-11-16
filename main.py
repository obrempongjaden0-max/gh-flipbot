from flask import Flask
import requests
from bs4 import BeautifulSoup
import time
import telegram
import os

app = Flask(__name__)
bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = ["iphone 13", "samsung a54", "nike air force 1"]
ALI_PRICES = {"iphone 13": 3800, "samsung a54": 2200, "nike air force 1": 650}

def scrape_jumia(kw):
    try:
        url = f"https://www.jumia.com.gh/catalog/?q={kw.replace(' ', '+')}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('article', class_='prd')[:3]
        return [{"name": i.find('h3').text.strip(), 
                 "price": float(i.find('div', class_='prc').text.replace('GH₵','').replace(',','')), 
                 "link": "https://www.jumia.com.gh" + i.find('a')['href']} for i in items if i.find('div', class_='prc')]
    except: return []

@app.route('/')
def home():
    html = "<h1>GH FlipBot LIVE</h1><p>Scanning every 30 mins...</p><ul>"
    for kw in KEYWORDS:
        for item in scrape_jumia(kw):
            profit = item["price"] - ALI_PRICES.get(kw, 0)
            if profit >= 200:
                html += f"<li>PROFIT GH₵{profit:.0f} → <a href='{item['link']}'>{item['name']}</a></li>"
    return html + "</ul><p>No deals? Check back in 30 mins.</p>"

def run():
    while True:
        for kw in KEYWORDS:
            ali = ALI_PRICES.get(kw, 0)
            for item in scrape_jumia(kw):
                profit = item["price"] - ali
                if profit >= 200:
                    msg = f"""FLIP ALERT
{kw.upper()}
Buy Ali: GH₵{ali}
Sell Jumia: GH₵{item['price']}
PROFIT: GH₵{profit:.0f}
{item['link']}"""
                    try: bot.send_message(chat_id=CHAT_ID, text=msg)
                    except: pass
        time.sleep(1800)

import threading
threading.Thread(target=run, daemon=True).start()
app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
