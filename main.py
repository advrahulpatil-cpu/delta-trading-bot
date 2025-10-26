from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    print("✅ Your trading bot is live and listening!")
    return "✅ Your trading bot is live and listening!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    headers = dict(request.headers)
    ip = request.remote_addr

    print("✅ Received webhook:", data)
    print("📡 Headers:", headers)
    print("🌍 IP Address:", ip)

    # Secret check
    if data.get("secret") != "rahul123":
        print(f"❌ Unauthorized: Invalid secret '{data.get('secret')}'")
        return jsonify({"status": "unauthorized"}), 403

    # Extract required fields
    side = data.get("side")
    quantity = data.get("quantity")
    order_type = data.get("type")

    if not all([side, quantity, order_type]):
        print("❌ Missing required fields in payload")
        return jsonify({"status": "bad request"}), 400

    print(f"📈 Executing {side.upper()} order for BTCUSDT: {quantity} units as {order_type.upper()}")
    place_order(side, quantity, order_type)

    return jsonify({"status": "success"}), 200

def place_order(side, quantity, order_type):
    url = "https://api.delta.exchange/v2/orders"
    headers = {
        "api-key": "Q9i261PfPdoY8hEBa5uxcjRTebWYsZ",  # ✅ Your live trading key
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
        print("📤 Order response:", response.json())
    except Exception as e:
        print("❌ Order failed:", str(e))

if __name__ == '__main__':
    print("🚀 Starting trading bot on port 10000...")
    app.run(host='0.0.0.0', port=10000)
