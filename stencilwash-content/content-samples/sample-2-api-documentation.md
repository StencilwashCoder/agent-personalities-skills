# Complete API Documentation: Building Developer-First APIs

## Introduction

Great products can fail because of poor documentation. When developers evaluate your API, they spend less than 5 minutes deciding if it's worth their time. Your documentation isn't just reference material—it's your primary sales tool.

This guide demonstrates what complete, developer-first API documentation looks like. We'll use a fictional payment API as our example, but these principles apply to any developer tool.

---

## Quick Start

### 1. Get Your API Keys

```bash
curl -X POST https://api.example.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dev@yourcompany.com",
    "organization": "Your Company"
  }'
```

Response:
```json
{
  "api_key": "pk_live_51H7x...",
  "api_secret": "sk_live_...",
  "webhook_secret": "whsec_..."
}
```

**Important**: Store your secret key securely. Never expose it in client-side code.

### 2. Make Your First Request

```bash
curl https://api.example.com/v1/health \
  -H "Authorization: Bearer pk_live_51H7x..."
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.2.0",
  "timestamp": "2026-03-27T10:30:00Z"
}
```

### 3. Create Your First Resource

```bash
curl -X POST https://api.example.com/v1/customers \
  -H "Authorization: Bearer pk_live_51H7x..." \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "name": "Jane Developer"
  }'
```

---

## Authentication

All API requests require authentication using your API key in the `Authorization` header.

### API Keys

| Key Type | Prefix | Environment | Permissions |
|----------|--------|-------------|-------------|
| Publishable | `pk_` | Client-side | Read-only, non-sensitive |
| Secret | `sk_` | Server-side | Full access |

```bash
# Correct
-H "Authorization: Bearer sk_live_..."

# Incorrect - never do this
?api_key=sk_live_...  # Don't pass in URL
```

### Request Signing (Optional)

For additional security on sensitive operations:

```javascript
import crypto from 'crypto';

function signRequest(payload, timestamp, secret) {
  const signature = crypto
    .createHmac('sha256', secret)
    .update(`${timestamp}.${JSON.stringify(payload)}`)
    .digest('hex');
  
  return `t=${timestamp},v1=${signature}`;
}

// Add to headers
-H "X-Signature: t=1711531800,v1=a1b2c3..."
```

---

## Core Resources

### Customers

Customers represent the individuals or businesses using your service.

#### Create a Customer

```http
POST /v1/customers
```

**Request Body:**
```json
{
  "email": "customer@example.com",
  "name": "Jane Developer",
  "metadata": {
    "plan": "pro",
    "signup_source": "documentation"
  }
}
```

**Response:**
```json
{
  "id": "cus_9sWWPAp9l8dK4x",
  "object": "customer",
  "email": "customer@example.com",
  "name": "Jane Developer",
  "created_at": 1711531800,
  "metadata": {
    "plan": "pro",
    "signup_source": "documentation"
  },
  "balance": 0,
  "currency": "usd"
}
```

#### Retrieve a Customer

```http
GET /v1/customers/:id
```

**Example:**
```bash
curl https://api.example.com/v1/customers/cus_9sWWPAp9l8dK4x \
  -H "Authorization: Bearer sk_live_..."
```

#### Update a Customer

```http
PATCH /v1/customers/:id
```

**Request Body:**
```json
{
  "name": "Jane Developer-Lead",
  "metadata": {
    "plan": "enterprise"
  }
}
```

**Note:** The `metadata` field is merged, not replaced.

#### List All Customers

```http
GET /v1/customers?limit=10&starting_after=cus_...
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Number of results (1-100, default 10) |
| `starting_after` | string | Cursor for pagination |
| `email` | string | Filter by email |
| `created[gte]` | timestamp | Filter by creation date |

**Response:**
```json
{
  "object": "list",
  "data": [...],
  "has_more": true,
  "next_cursor": "cus_..."
}
```

### Payments

#### Create a Payment

```http
POST /v1/payments
```

**Request Body:**
```json
{
  "amount": 2000,
  "currency": "usd",
  "customer": "cus_9sWWPAp9l8dK4x",
  "payment_method": "pm_card_visa",
  "description": "Payment for Invoice #1234",
  "metadata": {
    "order_id": "ord_5678"
  }
}
```

**Response:**
```json
{
  "id": "pay_1GqIC8A...",
  "object": "payment",
  "amount": 2000,
  "currency": "usd",
  "status": "succeeded",
  "customer": "cus_9sWWPAp9l8dK4x",
  "payment_method": "pm_card_visa",
  "description": "Payment for Invoice #1234",
  "metadata": {
    "order_id": "ord_5678"
  },
  "created_at": 1711531800,
  "receipt_url": "https://pay.example.com/rcpt/..."
}
```

#### Capture an Authorized Payment

```http
POST /v1/payments/:id/capture
```

**Request Body:**
```json
{
  "amount": 1500
}
```

Capture a portion of an authorized amount (partial capture).

#### Refund a Payment

```http
POST /v1/refunds
```

**Request Body:**
```json
{
  "payment": "pay_1GqIC8A...",
  "amount": 2000,
  "reason": "requested_by_customer"
}
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "card_declined",
    "message": "Your card was declined.",
    "decline_code": "insufficient_funds",
    "param": "payment_method",
    "request_id": "req_8Jwp8qB..."
  }
}
```

### Error Types

| Type | HTTP Status | Description |
|------|-------------|-------------|
| `api_error` | 500 | Internal server error |
| `authentication_error` | 401 | Invalid API key |
| `invalid_request_error` | 400 | Malformed request |
| `rate_limit_error` | 429 | Too many requests |
| `validation_error` | 422 | Invalid field value |

### Error Codes

Common error codes you'll encounter:

**Payment Errors:**
- `card_declined` - The card was declined
- `expired_card` - The card has expired
- `incorrect_cvc` - The CVC is incorrect
- `processing_error` - A processing error occurred

**Request Errors:**
- `resource_missing` - The requested resource doesn't exist
- `resource_already_exists` - Resource with this ID already exists
- `parameter_missing` - Required parameter is missing
- `parameter_invalid` - Parameter value is invalid

### Idempotency

Prevent duplicate operations using the `Idempotency-Key` header:

```bash
curl -X POST https://api.example.com/v1/payments \
  -H "Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer sk_live_..." \
  -d '{...}'
```

**Key properties:**
- Keys are unique per operation
- Retried requests with the same key return the original response
- Keys expire after 24 hours
- Safe to retry on network errors (5xx, timeouts)

---

## Rate Limits

API requests are limited to prevent abuse:

| Plan | Rate Limit |
|------|-----------|
| Free | 100 req/min |
| Pro | 1,000 req/min |
| Enterprise | 10,000 req/min |

**Rate limit headers:**

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1711531860
```

**Exceeding limits:**

```json
{
  "error": {
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "retry_after": 60
  }
}
```

**Best practices:**
- Implement exponential backoff
- Cache responses when possible
- Use webhooks instead of polling

---

## Webhooks

Webhooks notify your server when events occur.

### Setting Up Webhooks

1. **Configure endpoint in dashboard** or via API:

```bash
curl -X POST https://api.example.com/v1/webhook_endpoints \
  -H "Authorization: Bearer sk_live_..." \
  -d '{
    "url": "https://your-domain.com/webhooks",
    "enabled_events": ["payment.succeeded", "payment.failed"]
  }'
```

2. **Verify webhook signatures:**

```javascript
import crypto from 'crypto';

function verifyWebhook(payload, signature, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

### Event Types

| Event | Description |
|-------|-------------|
| `payment.succeeded` | Payment completed successfully |
| `payment.failed` | Payment failed |
| `payment.refunded` | Payment was refunded |
| `customer.created` | New customer created |
| `customer.updated` | Customer details changed |
| `invoice.paid` | Invoice was paid |

### Event Structure

```json
{
  "id": "evt_1GqIC8A...",
  "object": "event",
  "type": "payment.succeeded",
  "created": 1711531800,
  "data": {
    "object": {
      "id": "pay_1GqIC8A...",
      "object": "payment",
      "status": "succeeded",
      ...
    }
  }
}
```

**Important:** Webhooks may be delivered out of order. Use the `created` timestamp or event ID for ordering.

---

## SDKs & Libraries

### JavaScript/TypeScript

```bash
npm install @example/api
```

```typescript
import { ExampleAPI } from '@example/api';

const client = new ExampleAPI('sk_live_...');

// Create a customer
const customer = await client.customers.create({
  email: 'customer@example.com',
  name: 'Jane Developer'
});

// Create a payment
const payment = await client.payments.create({
  amount: 2000,
  currency: 'usd',
  customer: customer.id
});
```

### Python

```bash
pip install example-api
```

```python
from example_api import Client

client = Client('sk_live_...')

# Create a customer
customer = client.customers.create(
    email='customer@example.com',
    name='Jane Developer'
)

# Create a payment
payment = client.payments.create(
    amount=2000,
    currency='usd',
    customer=customer.id
)
```

### Go

```go
import "github.com/example/api-go/v1"

client := api.NewClient("sk_live_...")

// Create a customer
customer, err := client.Customers.Create(&api.CustomerParams{
    Email: "customer@example.com",
    Name:  "Jane Developer",
})

// Create a payment
payment, err := client.Payments.Create(&api.PaymentParams{
    Amount:   2000,
    Currency: "usd",
    Customer: customer.ID,
})
```

---

## Testing

### Test API Keys

Use test keys (prefix `pk_test_` / `sk_test_`) for development. No real charges are made.

### Test Card Numbers

| Number | Result |
|--------|--------|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 0002` | Card declined |
| `4000 0000 0000 9995` | Insufficient funds |
| `4000 0000 0000 0127` | Incorrect CVC |

### Test Webhooks

Use the CLI to trigger test events:

```bash
example trigger payment.succeeded
```

Or via API:

```bash
curl -X POST https://api.example.com/v1/events \
  -H "Authorization: Bearer sk_test_..." \
  -d '{
    "type": "payment.succeeded",
    "data": {
      "object": {
        "id": "pay_test_...",
        "amount": 2000
      }
    }
  }'
```

---

## Best Practices

### Security

1. **Never expose secret keys** in client-side code
2. **Use HTTPS** for all webhook endpoints
3. **Verify webhook signatures** to prevent spoofing
4. **Rotate keys** regularly (quarterly recommended)
5. **Use IP allowlisting** for webhook endpoints

### Performance

1. **Use idempotency keys** for all state-changing operations
2. **Implement caching** for frequently accessed data
3. **Use webhooks** instead of polling for state changes
4. **Batch operations** when possible
5. **Handle rate limits** with exponential backoff

### Reliability

1. **Handle errors gracefully** - don't crash on API errors
2. **Implement retries** with jitter for transient failures
3. **Log all requests** with request IDs for debugging
4. **Monitor webhook delivery** and retry failed deliveries
5. **Keep SDKs updated** for bug fixes and features

---

## Changelog

### v1.2.0 (2026-03-15)
- Added batch operations support
- New `metadata` field on all resources
- Improved webhook delivery reliability

### v1.1.0 (2026-02-01)
- Added customer portal sessions
- New payment method types: SEPA, ACH
- Improved error messages

### v1.0.0 (2026-01-15)
- Initial release
- Core payments functionality
- Webhook support

---

## Support

- **Documentation**: https://docs.example.com
- **Status Page**: https://status.example.com
- **Support Email**: support@example.com
- **Community Discord**: https://discord.gg/example

**API Status:** All systems operational

---

*This documentation was created by Stencilwash Content Agency. We specialize in developer-focused documentation that reduces support burden and drives adoption.*
