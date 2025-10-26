from flask import Flask, request, jsonify
import requests
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
    url = "https://api.delta.exchange/v2/orders"
    headers = {
        "api-key": "vSMdxAEBS7PwucaZYoINMJAEc8ePVC",  # ✅ Your new live trading key
        "Content-Type": "application/json"
    }
    payload = {
        "product_id": 24,  # BTCUSDT perpetual
        "size": quantity,
        "side": side,
        "order_type": order_type
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("📤 Order response:", response.json(), flush=True)
    except Exception as e:
        print("❌ Order failed:", str(e), flush=True)

if __name__ == '__main__':
    print("🚀 Starting trading bot on port 10000...", flush=True)
    sys.stdout.flush()
    app.run(host='0.0.0.0', port=10000)
