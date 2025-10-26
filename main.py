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

    # Log the received data
    print("✅ Received webhook:", data)

    # Extract trade details
    symbol = data.get("symbol")
    side = data.get("side")
    quantity = data.get("quantity")
    order_type = data.get("type")

    # Log the trade signal
    print(f"📈 Trade Signal → {side.upper()} {quantity} {symbol} as {order_type.upper()}")

    # Respond to TradingView
    return jsonify({"status": "success"}), 200

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
