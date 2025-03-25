from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Stock API is running! Use /stock/<symbol> to fetch stock prices."})

def fetch_stock_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        response = requests.get(url)
        data = response.json()
        print(f"✅ API Response: {data}")  # Debugging
        if "quoteResponse" in data and data["quoteResponse"]["result"]:
            return data["quoteResponse"]["result"][0]["regularMarketPrice"]
        else:
            raise Exception("Invalid response structure from Yahoo Finance")
    except Exception as e:
        print(f"❌ Error fetching stock data for {symbol}: {e}")
        raise


@app.route("/stock/<symbol>")
def get_stock(symbol):
    try:
        price = fetch_stock_price(symbol)
        return jsonify({"symbol": symbol, "price": price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
