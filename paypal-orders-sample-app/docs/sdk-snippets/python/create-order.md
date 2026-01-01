# Task: Create a PayPal Order

Create a PayPal order to start a checkout flow.

## Before You Start

- Python 3.9+

- PayPal Sandbox account

- Environment variables set:
  PAYPAL_CLIENT_ID=your_client_id
  PAYPAL_SECRET=your_secret

## Code Snippet (Python)

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://api-m.sandbox.paypal.com"

def get_access_token():
    response = requests.post(
        f"{BASE_URL}/v1/oauth2/token",
        auth=HTTPBasicAuth(
            client_id="YOUR_CLIENT_ID",
            password="YOUR_SECRET"
        ),
        data={"grant_type": "client_credentials"},
    )
    response.raise_for_status()
    return response.json()["access_token"]

def create_order():
    access_token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "10.00"
                }
            }
        ]
    }

    response = requests.post(
        f"{BASE_URL}/v2/checkout/orders",
        headers=headers,
        json=payload,
    )

    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    order = create_order()
    print(order)
