import time
import hmac
import hashlib
import json

def place_order(side, quantity, order_type):
    url_path = "/v2/orders"
    base_url = "https://api.india.delta.exchange"
    full_url = base_url + url_path

    api_key = "vSMdxAEBS7PwucaZYoINMJAEc8ePVC"
    api_secret = "qdtMbQCuRZ5A7039NlmIYOnYxTauiUAqEwCTSjUnFJDN2bSoSWUOAHjGIdDe"
    timestamp = str(int(time.time()))

    payload = {
        "product_id": 27,
        "size": quantity,
        "side": side,
        "order_type": order_type
    }

    # Use json.dumps with separators to match Delta's expected format
    body_str = json.dumps(payload, separators=(',', ':'))
    signature_payload = f"POST{timestamp}{url_path}{body_str}"
    signature = hmac.new(
        api_secret.encode(),
        signature_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "api-key": api_key,
        "timestamp": timestamp,
        "signature": signature,
        "User-Agent": "RahulBot",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(full_url, json=payload, headers=headers)
        print("📤 Order response:", response.json(), flush=True)
    except Exception as e:
        print("❌ Order failed:", str(e), flush=True)
