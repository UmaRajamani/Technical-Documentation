# API Flow – PayPal Orders & Webhooks 

This document explains the end-to-end payment flow using the PayPal Orders API and Webhooks.

Goal: One successful payment + one event.

## High-Level Flow

Client → Create Order

Buyer  → Approves Order

Server → Capture Order

PayPal → Sends Webhook

App    → Confirms Payment

## Step 1: Create Order

API

POST /v2/checkout/orders
### What happens

- Creates a payment intent

- No money moves

- Returns an order_id

### Why this step exists

- Separates intent from execution

- Enables async approval

- Success signal

  order_id returned

---

## Step 2: Buyer Approval

### Who owns this step

- PayPal UI

- Not your server

### What happens

- Buyer reviews and approves payment

- Approval may be delayed or retried

### Key concept

Approval is asynchronous.

---

## Step 3: Capture Order

API

POST /v2/checkout/orders/{order_id}/capture


### What happens

- Finalizes the payment

- Funds are transferred

- Order status becomes COMPLETED

### Success signal

status: COMPLETED

---

## Step 4: Webhook Event

Event

CHECKOUT.ORDER.APPROVED


### What PayPal does

- Sends an event to your webhook endpoint

- Confirms buyer approval

### Why this matters

- Client may disconnect

- Approval may happen later

- Webhooks are the source of truth

---

 ## Step 5: Application Response

### Your app

- Receives webhook

- Decides when to capture

- Updates internal systems

### Typical actions

- Trigger capture

- Update order status

- Notify downstream systems

---

## End-to-End Timeline

t0 → Order created

t1 → Buyer approves

t2 → Webhook received

t3 → Order captured

t4 → Payment confirmed

This timeline explains real-world behavior.


## Error Paths (Simplified)

|Scenario	               | Result           |  
|------------------------|------------------|
|Capture before approval |ORDER_NOT_APPROVED|
|Duplicate capture	     |Duplicate request error|
|Network failure         |Safe retry|

Errors are expected.The flow supports them.

## Why This Flow Works

- Supports async systems

- Prevents double charges

- Aligns with enterprise payment patterns

- Easy to reason about
