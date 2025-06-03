from flask import Flask, jsonify
import cloudscraper
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Grow a Garden stock API is running!"

@app.route('/stock')
def get_stock():
    scraper = cloudscraper.create_scraper()
    url = "https://www.vulcanvalues.com/grow-a-garden/stock"
    res = scraper.get(url)

    soup = BeautifulSoup(res.text, "html.parser")
    blocks = soup.find_all("div", class_="stock-block")

    if not blocks:
        return jsonify({"error": "Stock not found"})

    result = []
    for block in blocks:
        title = block.find("h2").text
        items = [li.text.strip() for li in block.find_all("li")]
        result.append({
            "shop": title,
            "items": items
        })

    return jsonify(result)
  
