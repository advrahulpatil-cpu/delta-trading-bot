from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is live"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("✅ Received webhook:", data)

    # Example logic: extract and print trade details
    symbol = data.get("symbol")
    side = data.get("side")
    quantity = data.get("quantity")
    order_type = data.get("type")

    print(f"📈 Trade Signal → {side.upper()} {quantity} {symbol} as {order_type.upper()}")

    # Respond to TradingView
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
