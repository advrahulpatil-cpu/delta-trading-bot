from fastapi import FastAPI, Request
import uvicorn
import hmac
import hashlib
import requests

app = FastAPI()

API_KEY = "your_delta_api_key"
API_SECRET = "your_delta_api_secret"
BASE_URL = "https://api.delta.exchange"
WEBHOOK_SECRET = "rahul123"

# ✅ Symbol-to-product_id mapping
symbol_to_product_id = {
    "BTCUSDT": 27,
    "ETHUSDT": 28
}

@app.get("/")
def root():
    return {"status": "ok"}

def generate_signature(api_secret, method, path, body):
    message = method + path + body
    return hmac.new(api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print(f"✅ Received webhook: {payload}")
    print(f"📡 Headers: {dict(request.headers)}")

    if payload.get("secret") != WEBHOOK_SECRET:
        return {"error": "Unauthorized"}

    side = payload.get("side")
    quantity = payload.get("quantity")
    order_type = payload.get("type")
    symbol = payload.get("symbol", "BTCUSDT")
    product_id = symbol_to_product_id.get(symbol, 27)

    path = "/v2/orders/create"
    url = BASE_URL + path
    body = {
        "order_type": order_type,
        "size": quantity,
        "side": side,
        "product_id": product_id
    }
    body_str = str(body).replace("'", '"')
    signature = generate_signature(API_SECRET, "POST", path, body_str)

    headers = {
        "api-key": API_KEY,
        "signature": signature,
        "Content-Type": "application/json"
    }

    print(f"📈 Executing {side.upper()} order for {symbol}: {quantity} units as {order_type.upper()}")
    response = requests.post(url, headers=headers, json=body)
    print(f"📤 Order response: {response.json()}")

    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
