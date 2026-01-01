import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
BASE_URL = "https://api-m.sandbox.paypal.com"

def get_access_token():
    response = requests.post(
        f"{BASE_URL}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )
    return response.json()["access_token"]

@app.route("/create-order")
def create_order():
    token = get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "10.00",
                }
            }
        ],
    }

    response = requests.post(
        f"{BASE_URL}/v2/checkout/orders",
        json=payload,
        headers=headers,
    )

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    return {
        "message": "PayPal Orders API sample app",
        "endpoints": [
            "/create-order",
            "/capture-order"
        ]
    }
