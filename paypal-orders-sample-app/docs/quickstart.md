# Create Your First PayPal Order in 5 Minutes (Python)

This guide helps you make your **first successful PayPal API call** using the
Orders API. By the end, you will create a PayPal order using runnable code.

---

## Prerequisites
- PayPal Developer account
- Python 3.9+
- Basic familiarity with REST APIs

---

## Step 1: Get PayPal Sandbox Credentials

1. Go to the PayPal Developer Dashboard
2. Create a Sandbox app
3. Copy the **Client ID** and **Secret**

---

## Step 2: Set Environment Variables

Create a `.env` file:

```bash
PAYPAL_CLIENT_ID=your_client_id_here
PAYPAL_SECRET=your_secret_here

---

## Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Start the Sample App
python app.py

The server runs at:

http://127.0.0.1:5000

Step 5: Create Your First Order
Call the endpoint:

curl http://127.0.0.1:5000/create-order
Expected Response

{
  "id": "5O190127TN364715T",
  "status": "CREATED"
}
