from flask import Flask, request, jsonify
import requests
import time
import hmac
import hashlib
import json
import sys

app = Flask(__name__)

@app.route('/')
def home():
    print("✅ Your trading bot is live and listening!", flush=True)
    return "✅ Your trading bot is live and listening!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    headers = dict(request.headers)
    ip = request.remote_addr

    print("✅ Received webhook:", data, flush=True)
    print("📡 Headers:", headers, flush=True)
    print("🌍 IP Address:", ip, flush=True)

    # Secret check
    if data.get("secret") != "rahul123":
        print(f"❌ Unauthorized: Invalid secret '{data.get('secret')}'", flush=True)
        return jsonify({"status": "unauthorized"}), 403

    # Extract required fields
    side = data.get("side")
    quantity = data.get("quantity")
    order_type = data.get("type")

    if not all([side, quantity, order_type]):
        print("❌ Missing required fields in payload", flush=True)
        return jsonify({"status": "bad request"}), 400

    print(f"📈 Executing {side.upper()} order for BTCUSDT: {quantity} units as {order_type.upper()}", flush=True)
    place_order(side, quantity, order_type)

    return jsonify({"status": "success"}), 200

def place_order(side, quantity, order_type):
    url_path = "/v2/orders"
    api_key = "ZrXkQYvZyWJvUQZJvXkQYvZyWJvUQZJv"  # Replace with your actual key if needed
    api_secret = "qdtMbQCuRZ5A7039NlmIYOnYxTauiUAqEwCTSjUnFJDN2bSoSWUOAHjGIdDe"
    timestamp = str(int(time.time()))

    # Fix order_type to match Delta's schema
    if order_type == "market":
        order_type = "market_order"
    elif order_type == "limit":
        order_type = "limit_order"

    payload = {
        "product_id": 27,
        "size": quantity,
        "side": side,
        "order_type": order_type
    }

    body_str = json.dumps(payload, separators=(',', ':'))
    signature_payload = f"POST{timestamp}{url_path}{body_str}"
    signature = hmac.new(
        api_secret.encode('utf-8'),
        signature_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "api-key": api_key,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"https://api.delta.exchange{url_path}",
            headers=headers,
            data=body_str
        )
        print("📤 Order response:", response.json(), flush=True)
    except Exception as e:
        print("❌ Order failed:", str(e), flush=True)

if __name__ == '__main__':
    print("🚀 Starting trading bot on port 10000...", flush=True)
    sys.stdout.flush()
    app.run(host='0.0.0.0', port=10000)