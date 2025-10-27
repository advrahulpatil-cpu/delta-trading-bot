from fastapi import FastAPI, Request
import hmac
import hashlib
import time
import requests

app = FastAPI()

API_KEY = "ZLG71WhzFyT1mPs8UWoMHGLAeX3WjL"
API_SECRET = "cIcjQ6tWsdia6LkluCpZBkJZw9z5zvhTzGq5Kmeh5X2IZnCqtPypafeAAzVC"
BASE_URL = "https://api.delta.exchange"

@app.get("/")
def root():
    return {"status": "lyra-delta-relay is live"}

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.get("/my-ip")
def get_ip():
    ip = requests.get("https://api64.ipify.org").text
    return {"outbound_ip": ip}

@app.post("/webhook")
async def webhook_listener(request: Request):
    payload = await request.json()
    timestamp = str(int(time.time() * 1000))
    signature_payload = timestamp + API_KEY
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        signature_payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }

    order_data = {
        "symbol": payload["symbol"],
        "side": payload["side"],
        "order_type": payload["type"],
        "size": payload["quantity"],
        "position_side": payload["position_side"],
        "reduce_only": payload["reduce_only"]
    }

    response = requests.post(f"{BASE_URL}/v2/orders", json=order_data, headers=headers)
    print("Received webhook:", payload)
    print("Order response:", response.status_code, response.text)

    return {"status": "order sent", "response": response.text}
