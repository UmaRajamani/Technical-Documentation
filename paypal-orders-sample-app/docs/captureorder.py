
import requests
import os

BASE_URL = "https://api-m.sandbox.paypal.com"

response = requests.post(
    f"{BASE_URL}/v1/oauth2/token",
    auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_SECRET")),
    data={"grant_type": "client_credentials"},
)

access_token = response.json()["access_token"]

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

order = requests.post(
    f"{BASE_URL}/v2/checkout/orders",
    headers=headers,
    json={
        "intent": "CAPTURE",
        "purchase_units": [
            {"amount": {"currency_code": "USD", "value": "10.00"}}
        ],
    },
)

print(order.json()["id"])

import requests

BASE_URL = "https://api-m.sandbox.paypal.com"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

response = requests.post(
    f"{BASE_URL}/v2/checkout/orders/{order_id}/capture",
    headers=headers,
)

print(response.json()["status"])

