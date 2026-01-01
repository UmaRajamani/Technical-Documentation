# Handle PayPal Webhooks

Webhooks notify your application when important events occur asynchronously.

---

## Supported Event
- CHECKOUT.ORDER.APPROVED

---

## Step 1: Expose a Public URL
Use a tool like ngrok:
```bash
ngrok http 5000
