# Handle PayPal Webhooks

Webhooks notify your application when important events occur asynchronously.

---

## Supported Event
- CHECKOUT.ORDER.APPROVED

---

## Step 1: Expose a Public URL
Use a tool like ngrok:

ngrok http 5000

---

## Step 2: Register Webhook URL

  1. Go to PayPal Developer Dashboard
  
  2. Add webhook URL
  
  3. Subscribe to CHECKOUT.ORDER.APPROVED

---

## Step 3: Verify Event Delivery

When an order is approved, PayPal sends a POST request to /webhook.

---

## Best Practices

- Always return HTTP 200

- Log event IDs

- Validate webhook signatures in production
