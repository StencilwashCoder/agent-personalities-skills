# From Zero to Production: Deploying on Kubernetes

*Part 1 of 5: Understanding Kubernetes Fundamentals*

---

## Introduction

Kubernetes has become the de facto standard for container orchestration. Whether you're a startup preparing for scale or an enterprise modernizing your infrastructure, understanding Kubernetes is essential for production deployments.

This tutorial series will take you from zero Kubernetes knowledge to running a production-ready application. In this first part, we'll cover the core concepts you need to understand before deploying anything.

---

## What is Kubernetes?

Kubernetes (Greek for "helmsman") is an open-source container orchestration platform originally developed by Google. It automates the deployment, scaling, and management of containerized applications.

### Why Kubernetes?

**Before Kubernetes:**
```
Developer: "It works on my machine"
Ops: "Your machine isn't production"
[Hours of configuration drift debugging...]
```

**With Kubernetes:**
```
Developer: "Here's my container image"
Kubernetes: "I'll make sure it runs the same way everywhere"
```

### Key Benefits

1. **Declarative Configuration**: Describe what you want, not how to get there
2. **Self-Healing**: Automatically restarts failed containers, reschedules, and replaces
3. **Horizontal Scaling**: Scale applications up or down with simple commands
4. **Service Discovery**: Built-in load balancing and service discovery
5. **Rolling Updates**: Deploy new versions without downtime

---

## Core Concepts

### The Kubernetes Cluster Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLUSTER                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                   Control Plane                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │ API      │  │ Scheduler│  │ etcd     │          │  │
│  │  │ Server   │  │          │  │ (state)  │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  │  ┌──────────┐  ┌──────────┐                        │  │
│  │  │ Controller│  │ Cloud    │                        │  │
│  │  │ Manager  │  │ Manager  │                        │  │
│  │  └──────────┘  └──────────┘                        │  │
│  └─────────────────────────────────────────────────────┘  │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                   Worker Nodes                       │  │
│  │  ┌──────────────┐  ┌──────────────┐                │  │
│  │  │ Node 1       │  │ Node 2       │  ...           │  │
│  │  │ ┌──────────┐ │  │ ┌──────────┐ │                │  │
│  │  │ │ Pod A    │ │  │ │ Pod C    │ │                │  │
│  │  │ │ Pod B    │ │  │ │ Pod D    │ │                │  │
│  │  │ └──────────┘ │  │ └──────────┘ │                │  │
│  │  │ kubelet      │  │ kubelet      │                │  │
│  │  │ kube-proxy   │  │ kube-proxy   │                │  │
│  │  └──────────────┘  └──────────────┘                │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### The Pod: Kubernetes's Smallest Deployable Unit

A **Pod** is the basic building block of Kubernetes. It represents a single instance of a running process in your cluster.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod
  labels:
    app: web
spec:
  containers:
  - name: nginx
    image: nginx:1.25
    ports:
    - containerPort: 80
```

**Key characteristics:**
- Pods can contain multiple containers (sidecar pattern)
- Containers in a pod share the same network namespace
- Pods are ephemeral—expect them to die and be recreated

### Deployments: Managing Pod Lifecycles

While you *can* create Pods directly, you rarely should. **Deployments** manage ReplicaSets, which manage Pods.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3  # Run 3 instances
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
```

**What this gives you:**
- Automatic Pod replacement if one dies
- Rolling updates when you change the image
- Easy scaling: `kubectl scale deployment web-deployment --replicas=5`

### Services: Exposing Your Applications

Pods are ephemeral—they get new IPs when recreated. **Services** provide stable networking.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web  # Targets pods with this label
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP  # Internal cluster access only
```

**Service Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| `ClusterIP` | Internal cluster IP only | Internal microservices |
| `NodePort` | Exposes on each node's IP at a static port | Direct node access |
| `LoadBalancer` | Exposes externally using cloud load balancer | Production web apps |
| `ExternalName` | Maps to external DNS | External dependencies |

### ConfigMaps and Secrets: Configuration Management

**ConfigMaps** store non-sensitive configuration:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgres://db:5432/myapp"
  LOG_LEVEL: "info"
  FEATURE_FLAGS: "new_ui=true,api_v2=true"
```

**Secrets** store sensitive data (base64 encoded, not encrypted):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: cGFzc3dvcmQxMjM=  # echo -n 'password123' | base64
  API_KEY: bXlzZWNyZXRrZXk=
```

**Using them in Pods:**

```yaml
spec:
  containers:
  - name: web
    image: myapp:v1.0.0
    envFrom:
    - configMapRef:
        name: app-config
    env:
    - name: DATABASE_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: DATABASE_PASSWORD
```

---

## Your First Kubernetes Deployment

### Prerequisites

1. **Install kubectl** (Kubernetes CLI):
```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s/release/$(curl -L -s https://dl.k8s/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```

2. **Install a local cluster** (for development):
```bash
# Option 1: Docker Desktop (enable Kubernetes in settings)
# Option 2: minikube
brew install minikube
minikube start

# Option 3: kind (Kubernetes in Docker)
brew install kind
kind create cluster
```

### Deploy a Sample Application

**Step 1: Create the Deployment**

```yaml
# web-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-k8s
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello
  template:
    metadata:
      labels:
        app: hello
    spec:
      containers:
      - name: hello
        image: paulbouwer/hello-kubernetes:1.10
        ports:
        - containerPort: 8080
        env:
        - name: MESSAGE
          value: "Hello from Kubernetes!"
```

**Step 2: Apply the Deployment**

```bash
kubectl apply -f web-deployment.yaml
```

**Step 3: Verify**

```bash
# Check deployment
kubectl get deployments

# Check pods
kubectl get pods

# Detailed pod info
kubectl describe pods
```

**Step 4: Expose the Service**

```yaml
# web-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  selector:
    app: hello
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

```bash
kubectl apply -f web-service.yaml

# For local clusters, use port-forwarding
kubectl port-forward service/hello-service 8080:80
```

**Visit:** http://localhost:8080

### Basic kubectl Commands

```bash
# View all resources
kubectl get all

# View logs
kubectl logs <pod-name>

# Follow logs
kubectl logs -f <pod-name>

# Execute command in container
kubectl exec -it <pod-name> -- /bin/sh

# Scale deployment
kubectl scale deployment hello-k8s --replicas=5

# Update image
kubectl set image deployment/hello-k8s hello=nginx:latest

# Rollback
kubectl rollout undo deployment/hello-k8s

# Check rollout status
kubectl rollout status deployment/hello-k8s

# Delete resources
kubectl delete -f web-deployment.yaml
```

---

## Understanding kubectl Contexts

You'll likely work with multiple clusters (local, staging, production). **Contexts** make switching easy:

```bash
# List contexts
kubectl config get-contexts

# Switch context
kubectl config use-context production

# Set namespace for current context
kubectl config set-context --current --namespace=myapp

# View current config
kubectl config view
```

**Pro tip:** Use [kubectx](https://github.com/ahmetb/kubectx) and [kubens](https://github.com/ahmetb/kubectx) for easier context/namespace switching:

```bash
brew install kubectx

kubectx production  # Switch context
kubens monitoring   # Switch namespace
```

---

## Namespaces: Isolation and Organization

Namespaces provide a scope for names. They're useful for:
- Separating environments (dev, staging, prod)
- Multi-tenancy
- Resource organization

```bash
# Create namespace
kubectl create namespace production

# Deploy to specific namespace
kubectl apply -f deployment.yaml -n production

# View resources in namespace
kubectl get pods -n production

# Set default namespace
kubectl config set-context --current --namespace=production
```

---

## Common Beginner Mistakes

### 1. Forgetting Resource Limits

```yaml
# BAD: No resource limits
spec:
  containers:
  - name: app
    image: myapp:latest

# GOOD: Defined limits
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

Without limits, a runaway pod can consume all cluster resources.

### 2. Using `latest` Tag

```yaml
# BAD: Non-deterministic deployments
image: myapp:latest

# GOOD: Immutable tags
image: myapp:v1.2.3
```

`latest` makes rollbacks impossible and leads to "works on my cluster" issues.

### 3. Ignoring Health Checks

```yaml
# Add liveness and readiness probes
spec:
  containers:
  - name: app
    image: myapp:v1.0.0
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
```

### 4. Storing Secrets in Git

```yaml
# BAD: Secrets in version control
env:
- name: DATABASE_PASSWORD
  value: "supersecret123"

# GOOD: Use Kubernetes Secrets
env:
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: password
```

Consider using [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or [External Secrets Operator](https://external-secrets.io/) for GitOps workflows.

---

## What's Next?

In Part 2, we'll cover:
- **Ingress Controllers**: HTTP routing and SSL termination
- **Persistent Storage**: Volumes and StatefulSets
- **Configuration Management**: Helm charts
- **Monitoring**: Prometheus and Grafana setup

---

## Additional Resources

- **Official Kubernetes Documentation**: https://kubernetes.io/docs
- **Kubernetes by Example**: https://kubernetesbyexample.com
- **Katacoda Scenarios**: https://katacoda.com/courses/kubernetes
- **Play with Kubernetes**: https://labs.play-with-k8s.com

---

*This tutorial series is brought to you by Stencilwash Content Agency. We create technical content that helps developers succeed.*
