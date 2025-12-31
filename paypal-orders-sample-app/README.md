# PayPal Orders API – Sample App (Python)

This sample application demonstrates how to:
- Authenticate with PayPal REST APIs
- Create and capture an order using the Orders API
- Design documentation to reduce time-to-first API call

## Prerequisites
- PayPal developer account
- Python 3.9+
- Sandbox credentials

## Quick Start
1. Clone the repo
2. Create `.env` file
3. Run `pip install -r requirements.txt`
4. Start server and call `/create-order`

## API Flow
1. Client requests `/create-order`
2. App requests OAuth token
3. App calls PayPal Orders API
4. PayPal returns order ID

## Developer Experience Focus
- Runnable code snippets
- Clear error handling
- Minimal setup steps

