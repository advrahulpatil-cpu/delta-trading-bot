from fastapi import FastAPI, Request
import hmac
import hashlib
import time
import requests

app = FastAPI()

API_KEY = "your_new_api_key"
API_SECRET = "your_new_api_secret"

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

    # Example order execution logic (replace with your actual flow)
    print("Received webhook:", payload)
    print("Generated signature:", signature)

    return {"status": "webhook received"}
