from flask import Flask, jsonify
import cloudscraper
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Grow a Garden API is running!"

@app.route('/stock')
def stock():
    scraper = cloudscraper.create_scraper()
    res = scraper.get("https://www.vulcanvalues.com/grow-a-garden/stock")
    soup = BeautifulSoup(res.text, 'html.parser')
    blocks = soup.find_all('div', class_='stock-block')

    result = []
    for block in blocks:
        title_tag = block.find("h2")
        items = block.find_all("li")

        if title_tag and items:
            result.append({
                "shop": title_tag.text.strip(),
                "items": [li.text.strip() for li in items]
            })

    return jsonify(result or {"error": "Stock not found"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render передаёт порт в переменной PORT
    app.run(host="0.0.0.0", port=port)
    
