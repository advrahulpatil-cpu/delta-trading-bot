import time
import hmac
import hashlib
import requests
import json
import threading
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your actual credentials
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
BASE_URL = "https://api.delta.exchange"

def generate_signature(api_secret, method, path, body):
    timestamp = str(int(time.time()))
    message = timestamp + method + path + (body or "")
    signature = hmac.new(
        api_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature, timestamp

def place_order(order_data):
    path = "/v2/orders/create"
    method = "POST"
    body = json.dumps(order_data)
    signature, timestamp = generate_signature(API_SECRET, method, path, body)

    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }

    url = BASE_URL + path
    response = requests.post(url, headers=headers, data=body)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "error": "Empty or invalid response",
            "status_code": response.status_code,
            "text": response.text
        }

@app.get("/")
async def root():
    return {"status": "lyra-delta-relay is live and listening on /webhook"}

@app.post("/webhook")
async def webhook_handler(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        return {"error": "Invalid JSON payload", "details": str(e)}

    print(f"Received webhook: {payload}")

    if payload.get("secret") != "rahul123":
        return {"error": "Invalid secret"}

    order_payload = {
        "symbol": payload["symbol"],
        "side": payload["side"],
        "order_type": payload["type"],
        "size": payload["quantity"],
        "position_side": payload["position_side"],
        "reduce_only": payload["reduce_only"]
    }

    result = place_order(order_payload)
    print(f"Order response: {result}")
    return result

# Keep-alive thread to prevent Render idle shutdown
def keep_alive():
    while True:
        try:
            requests.get("https://lyra-delta-relay.onrender.com/")
        except:
            pass
        time.sleep(240)

threading.Thread(target=keep_alive, daemon=True).start()
