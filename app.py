from flask import Flask, jsonify
import requests

app = Flask(__name__)

def fetch_stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    response = requests.get(url)
    data = response.json()

    # Check if response contains valid data
    results = data.get("quoteResponse", {}).get("result", [])
    if not results:
        return None  # No data found

    return results[0].get("regularMarketPrice")

@app.route("/")
def home():
    return jsonify({"message": "Stock API is running! Use /stock/<symbol> to fetch stock prices."})

@app.route("/stock/<symbol>")
def get_stock(symbol):
    try:
        price = fetch_stock_price(symbol)
        if price is None:
            return jsonify({"error": "Invalid stock symbol or no data available"}), 404

        return jsonify({"symbol": symbol, "price": price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Change to debug=False in production
