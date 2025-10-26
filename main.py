from flask import Flask, request, jsonify

app = Flask(__name__)

# Health check route
@app.route('/')
def home():
    return "✅ Your service is live 🎉"

# Webhook route for TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    headers = dict(request.headers)
    ip = request.remote_addr

    print("✅ Received webhook:", data)
    print("📡 Headers:", headers)
    print("🌍 IP Address:", ip)

    # Optional: Secret key check (add to your TradingView alert JSON)
    if data.get("secret") != "rahul123":
        print("❌ Invalid source: missing or wrong secret")
        return jsonify({"status": "unauthorized"}), 403

    # Extract trade details
    symbol = data.get("symbol")
    side = data.get("side")
    quantity = data.get("quantity")
    order_type = data.get("type")

    print(f"📈 Trade Signal → {side.upper()} {quantity} {symbol} as {order_type.upper()}")

    return jsonify({"status": "success"}), 200

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
