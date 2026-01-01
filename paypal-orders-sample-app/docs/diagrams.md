
# High-Level Payment Flow

┌──────────┐
│  Client  │
└────┬─────┘
     │ Create Order
     ▼
┌──────────────┐
│ PayPal API   │
└────┬─────────┘
     │ Order ID
     ▼
┌──────────────┐
│ Buyer (UI)   │
└────┬─────────┘
     │ Approves
     ▼
┌──────────────┐
│ Webhook      │◄───────────────┐
│ Listener     │                │
└────┬─────────┘                │
     │ Capture Order             │
     ▼                           │
┌──────────────┐                 │
│ PayPal API   │─────────────────┘
└──────────────┘
