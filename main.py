from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
TRADE_SIZE = 50
BASE_URL = "https://api.delta.exchange"

def place_order(symbol, side):
    url = f"{BASE_URL}/v2/orders"
    headers = {
        "api-key": API_KEY,
        "api-secret": API_SECRET,
        "Content-Type": "application/json"
    }
    data = {
        "product_id": symbol,
        "size": TRADE_SIZE,
        "side": side,
        "order_type": "market"
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Order response: {response.text}")
    return response.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(f"Received alert: {data}")
    message = data.get("message", "").lower()
    if "long" in message:
        place_order(symbol=extract_symbol(message), side="buy")
    elif "short" in message:
        place_order(symbol=extract_symbol(message), side="sell")
    return "OK", 200

def extract_symbol(message):
    coin = message.split()[0].upper()
    return f"{coin}USDT"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
