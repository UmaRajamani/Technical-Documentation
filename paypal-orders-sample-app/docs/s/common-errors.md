# Common Errors and How to Resolve Them

**1. Authentication Errors (401 Unauthorized)**

   **Cause**

   - Invalid Client ID or Secret

   - Sandbox credentials used in Live environment

   **Resolution**

   - Verify environment variables

   - Ensure Sandbox endpoint is used

**2. Invalid Request Payload (400 Bad Request)**

   **Cause**
    
   - Missing required fields
    
   - Incorrect currency or amount format
    
   **Resolution**
    
   - Validate request body
    
   - Use example payload from Quickstart
    
  
**3. Order Capture Fails**

   **Cause**
  
   - Order not approved
    
   - Duplicate capture attempt
  
   **Resolution**
  
   - Check order status before capture
    
   - Implement idempotency in production

**4. Webhook Not Received**

**Cause**

- Webhook URL not publicly accessible

- Event not subscribed

**Resolution**

- Use ngrok or similar

- Verify webhook subscription in dashboard
   
