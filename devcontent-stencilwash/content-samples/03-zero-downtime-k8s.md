# Zero-Downtime Deployments with Kubernetes

## The 3 AM Wake-Up Call

"Production is down."

Four words no engineer wants to hear. Especially when you just deployed a "harmless" config change. The rollback is taking forever. Customers are angry. Your manager is asking questions in Slack.

This guide covers battle-tested Kubernetes deployment patterns that keep services running during updates—even when things go wrong.

## The Basics: Rolling Updates

Kubernetes defaults to rolling updates. Good start, but not enough.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Start 1 new pod before removing old
      maxUnavailable: 0  # Never have fewer than 3 available
  template:
    spec:
      containers:
      - name: api
        image: myapp:v1.2.3
        readinessProbe:  # Critical: don't receive traffic until ready
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

The `readinessProbe` is non-negotiable. Without it, new pods receive traffic before they're ready to handle it.

## Pattern 1: Blue-Green Deployments

Two identical environments. Switch traffic instantly.

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-blue
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: myapp:v1.2.3

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-green
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: myapp:v1.3.0
```

Switch traffic by updating the Service selector:

```bash
# Switch to green
kubectl patch service api -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback to blue (instant)
kubectl patch service api -p '{"spec":{"selector":{"version":"blue"}}}'
```

**When to use**: Critical services where rollback speed matters more than resource efficiency.

## Pattern 2: Canary Deployments

Route 1% of traffic to new version. Watch metrics. Gradually increase.

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-canary
spec:
  hosts:
  - api.example.com
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: api
        subset: v2
      weight: 100
  - route:
    - destination:
        host: api
        subset: v1
      weight: 95
    - destination:
        host: api
        subset: v2
      weight: 5
```

Monitor these metrics during canary:

```promql
# Error rate spike?
rate(http_requests_total{status=~"5.."}[1m]) 
/ rate(http_requests_total[1m])

# Latency increase?
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[1m])
)

# Memory leak?
container_memory_usage_bytes{pod=~"api-v2-.*"}
```

Auto-rollback if thresholds exceeded:

```bash
#!/bin/bash
# Automated canary rollback

ERROR_RATE=$(kubectl exec deploy/prometheus -- \
  promql 'rate(http_5xx[1m])' | jq '.[0].value[1]')

if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
  echo "Canary failing. Rolling back..."
  kubectl patch virtualservice api-canary --type=merge \
    -p '{"spec":{"http":[{"route":[{"destination":{"subset":"v1"},"weight":100}]}]}}'
fi
```

## Pattern 3: Pod Disruption Budgets

Prevent Kubernetes from evicting too many pods at once.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2      # Always keep 2 pods running
  selector:
    matchLabels:
      app: api
```

Without this, a node drain during deployment could take down your entire service.

## Database Migrations: The Hard Part

Zero-downtime deployments fail when migrations lock tables.

### The Expand-Contract Pattern

```sql
-- Phase 1: Expand (deploy 1)
-- Add new column, keep old one
ALTER TABLE users ADD COLUMN email_normalized VARCHAR(255);

-- Backfill in batches (no table lock)
UPDATE users 
SET email_normalized = LOWER(email)
WHERE id BETWEEN 1 AND 10000;

-- Phase 2: Migrate (deploy 2)
-- Write to both columns
INSERT INTO users (email, email_normalized) 
VALUES ('USER@EXAMPLE.COM', 'user@example.com');

-- Phase 3: Contract (deploy 3)
-- Remove old column
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_normalized TO email;
```

Each phase is backward-compatible. Rollback any time.

## Health Checks Done Right

```yaml
livenessProbe:   # Restart if dead
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:  # Remove from load balancer if not ready
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5

startupProbe:    # Give slow-starting apps time
  httpGet:
    path: /health/startup
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

**Rule**: Liveness kills the pod. Readiness removes from traffic. Don't confuse them.

## Pre-Stop Hooks for Graceful Shutdown

```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 15"]
```

This delay lets the pod finish in-flight requests before Kubernetes sends SIGTERM.

## Deployment Checklist

Before shipping to production:

- [ ] Readiness probes configured and tested
- [ ] Liveness probes (if needed) don't overlap readiness
- [ ] Pod Disruption Budget defined
- [ ] Resource limits set (prevent noisy neighbor)
- [ ] Graceful shutdown handling implemented
- [ ] Database migrations are backward-compatible
- [ ] Rollback procedure documented and tested
- [ ] Monitoring dashboards ready
- [ ] Alerting rules configured

## Common Failure Modes

### The "Thud" Deployment

New pods start, immediately crash, Kubernetes keeps trying forever.

**Fix**: Set `progressDeadlineSeconds` to fail fast:

```yaml
spec:
  progressDeadlineSeconds: 300  # Fail deployment if no progress in 5 min
```

### The Resource Starvation

New pods won't schedule because nodes are full. Rolling update hangs.

**Fix**: Cluster autoscaler + pod priority:

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: production-high
value: 1000000
globalDefault: false
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      priorityClassName: production-high
```

## Conclusion

Zero-downtime deployments aren't about perfect code—they're about graceful failure. Assume your new version is broken. Design the deployment so users never notice.

Start with rolling updates and proper health checks. Add canary deployments for critical services. Always have a one-command rollback.

And maybe—just maybe—you'll sleep through the night.

---

*Want help hardening your Kubernetes deployments? [Let's chat](/contact).*
