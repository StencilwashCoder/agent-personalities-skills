# Observability-Driven Development

## "It Works on My Machine"

The most expensive words in software engineering.

You've deployed. Tests passed. Code reviewed. And yet—production is on fire. Users are complaining. Logs are a sea of noise. You don't know what's broken, only that something is.

This is what happens when observability is an afterthought. Let's fix that.

## The Three Pillars (and Why They're Not Enough)

Everyone talks about logs, metrics, and traces. They're table stakes.

- **Logs**: What happened (events)
- **Metrics**: How much/many (numbers over time)  
- **Traces**: Where it happened (request flow)

But the fourth pillar is what separates debugging from understanding: **context**.

## Observability-Driven Development (ODD)

Build systems that explain themselves. Every feature ships with:
1. A way to verify it's working
2. A way to know when it breaks
3. A way to understand why

## Instrumentation First, Code Second

### The Checklist Before You Commit

```typescript
// Before: "I'll add monitoring later"
async function processPayment(orderId: string, amount: number) {
  const result = await stripe.charges.create({ amount, ... });
  await db.orders.update(orderId, { status: 'paid' });
  return result;
}

// After: Observable from day one
async function processPayment(orderId: string, amount: number) {
  const span = tracer.startSpan('processPayment', {
    attributes: { orderId, amount }
  });
  
  try {
    const result = await stripe.charges.create({ amount, ... });
    
    logger.info('Payment processed', { 
      orderId, 
      chargeId: result.id,
      duration: span.duration 
    });
    
    metrics.increment('payment.success', { currency: result.currency });
    
    await db.orders.update(orderId, { status: 'paid' });
    
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
    
  } catch (error) {
    logger.error('Payment failed', { 
      orderId, 
      error: error.message,
      errorCode: error.code 
    });
    
    metrics.increment('payment.failure', { 
      errorType: error.type 
    });
    
    span.recordException(error);
    span.setStatus({ 
      code: SpanStatusCode.ERROR, 
      message: error.message 
    });
    
    throw error;
  } finally {
    span.end();
  }
}
```

## Structured Logging: The Foundation

Stop parsing strings. Log structured data.

### Bad

```
2024-01-15 14:23:01 INFO Server started on port 3000
2024-01-15 14:23:45 ERROR User login failed for user@example.com
```

### Good

```json
{
  "timestamp": "2024-01-15T14:23:01Z",
  "level": "info",
  "message": "Server started",
  "service": "api-gateway",
  "port": 3000,
  "version": "1.2.3",
  "host": "api-01"
}

{
  "timestamp": "2024-01-15T14:23:45Z",
  "level": "error",
  "message": "Authentication failed",
  "service": "auth-service",
  "userId": "user_123",
  "errorType": "InvalidCredentials",
  "attemptNumber": 3,
  "ipAddress": "192.168.1.100",
  "traceId": "abc123def456"
}
```

Query power: `errorType:InvalidCredentials AND attemptNumber>2`

## Correlation IDs: Following the Trail

```typescript
// Middleware attaches trace ID to every request
app.use((req, res, next) => {
  req.traceId = req.headers['x-trace-id'] || generateUUID();
  res.setHeader('x-trace-id', req.traceId);
  
  // All logs in this request include the trace ID
  req.logger = logger.child({ traceId: req.traceId });
  
  next();
});

// Propagate to downstream services
async function callUserService(userId: string, traceId: string) {
  return fetch(`https://users.internal/${userId}`, {
    headers: { 'x-trace-id': traceId }
  });
}
```

Now a single trace ID follows a request through 10 services.

## The RED Method: Metrics That Matter

For every service, track:

- **Rate**: Requests per second
- **Errors**: Error rate percentage  
- **Duration**: Request latency (p50, p95, p99)

```promql
# Rate
rate(http_requests_total[1m])

# Error rate  
rate(http_requests_total{status=~"5.."}[1m]) 
/ rate(http_requests_total[1m])

# Duration
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[1m])
)
```

Alert on these. Not CPU usage. Not memory. These.

## Distributed Tracing: See the Whole Picture

```typescript
// Automatic trace propagation
const tracer = opentelemetry.trace.getTracer('payment-service');

async function processOrder(orderId: string) {
  return tracer.startActiveSpan('processOrder', async (span) => {
    span.setAttribute('order.id', orderId);
    
    // This call gets its own child span automatically
    const user = await getUser(orderId);
    
    // And this one too
    const payment = await processPayment(orderId, user);
    
    span.setAttribute('payment.id', payment.id);
    
    return { user, payment };
  });
}
```

Result in Jaeger/Tempo:

```
processOrder (450ms)
├── getUser (50ms)
│   └── SELECT * FROM users (45ms)
├── validateInventory (100ms)
│   ├── checkStock (40ms)
│   └── reserveStock (60ms)
└── processPayment (300ms)
    └── stripe.charges.create (295ms)
```

The 295ms Stripe call jumps out immediately.

## Error Budgets: SLOs in Practice

```yaml
# Define what "good" looks like
api_availability:
  slo: 99.9%  # 43 minutes downtime/month acceptable
  window: 30d
  
api_latency:
  slo: 95% of requests < 200ms
  window: 30d
```

```typescript
// Burn rate alerting
// Fast burn: 2% budget in 1 hour → page immediately
// Slow burn: 5% budget in 6 hours → alert during business hours

const errorBudget = calculateErrorBudget(
  slo: 0.999,
  actual: measuredAvailability
);

if (errorBudget.burnRate > 14.4) {  // 2% in 1 hour
  pageOnCallEngineer();
}
```

## Alerting: Less Noise, More Signal

### Bad Alerts (Page Fatigue)

- "CPU usage > 80%"
- "Memory usage high"
- "Disk space < 20%"

### Good Alerts (Action Required)

- "Error rate > 1% for 5 minutes"
- "p95 latency > 500ms for 10 minutes"
- "Payment success rate < 95%"

**Rule**: If you get paged, there must be an action to take.

## The ODD Workflow

```
1. Write the feature
2. Add instrumentation (logs, metrics, traces)
3. Deploy to staging
4. Verify instrumentation works (see the data)
5. Add alerts for failure modes
6. Deploy to production
7. Verify alerts work (test with synthetic failures)
```

No feature is "done" until you can debug it in production.

## Tools We Use

| Layer | Tool | Purpose |
|-------|------|---------|
| Logs | Loki / Datadog | Structured log aggregation |
| Metrics | Prometheus | Time-series metrics |
| Traces | Tempo / Jaeger | Distributed tracing |
| Dashboards | Grafana | Visualization |
| Alerting | PagerDuty / Opsgenie | Incident response |
| APM | Datadog / New Relic | Full-stack observability |

## Cost Control

Observability data grows exponentially. Control costs:

```yaml
# Sample high-volume, low-value logs
logging:
  sampling:
    health_checks: 0.01    # Keep 1% of /health logs
    static_assets: 0.001   # Keep 0.1% of asset requests
    
# Drop debug logs in production
filters:
  - drop:
      severity: debug
      unless_trace_sampled: true
```

## Conclusion

Observability isn't a luxury—it's a requirement for production systems. The cost of adding it later is 10x the cost of building it in from the start.

Build systems that explain themselves. Instrument everything. Alert on symptoms, not causes. And never deploy on a Friday without confidence you can debug what breaks.

Because something always breaks.

---

*Need help implementing observability in your stack? [Let's chat](/contact).*
