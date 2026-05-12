# TARDIS Sovereign - Civo Cloud Deployment

UK-sovereign Kubernetes deployment on Civo Cloud (LON1 region).
Designed to run on GBP 250 of credits for as long as possible.

## Architecture

```
                         Internet
                            |
                     [ Civo Firewall ]
                      (80, 443, 6443)
                            |
               +------------+------------+
               |    Civo Kubernetes      |
               |    (k3s, LON1, UK)      |
               |                         |
               |  +-------------------+  |
               |  | Traefik Ingress   |  |
               |  | (TLS termination) |  |
               |  +---------+---------+  |
               |            |            |
               |  +---------+---------+  |
               |  | ClusterIP Service |  |
               |  +---------+---------+  |
               |            |            |
               |  +---------+---------+  |
               |  | sovereign-dispatch|  |
               |  | (1 replica,       |  |
               |  |  50m CPU,         |  |
               |  |  64-256Mi RAM)    |  |
               |  +-------------------+  |
               |                         |
               |  Node: g4s.kube.small   |
               |  Node: g4s.kube.small   |
               +-------------------------+
```

## Cost Estimates

| Resource               | Monthly Cost (GBP) |
|------------------------|---------------------|
| k3s cluster (2 nodes)  | ~20.00              |
| g4s.kube.small x2      | (included above)    |
| Network / Firewall     | 0.00                |
| Traefik (pre-installed)| 0.00                |
| **Total**              | **~20.00/month**    |

With GBP 250 credits: **~12 months of operation.**

To reduce costs further:
- Scale to 1 node (loses HA): saves ~GBP 10/month
- Use `g4s.kube.xsmall` if available: may save a few pounds

## Prerequisites

- [Civo CLI](https://www.civo.com/docs/overview/civo-cli) or API key
- [Terraform](https://terraform.io) >= 1.5
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Docker](https://docs.docker.com/get-docker/)

## Quick Start

### 1. Set your Civo API token

```bash
export TF_VAR_civo_token="YOUR_CIVO_API_KEY"
```

Get your key from: https://dashboard.civo.com/security

### 2. Deploy everything

```bash
cd infrastructure/civo
chmod +x deploy.sh
./deploy.sh apply
```

This will:
1. Provision a 2-node k3s cluster in LON1 via Terraform
2. Build the sovereign-dispatch Docker image
3. Apply all Kubernetes manifests

### 3. Configure secrets (important)

Edit `k8s/secrets.yaml` and replace the `PLACEHOLDER_*` values, or create
secrets directly:

```bash
export KUBECONFIG=./kubeconfig
kubectl create secret generic sovereign-dispatch-secrets \
  --namespace=tardis-sovereign \
  --from-literal=civo-api-key=YOUR_CIVO_KEY \
  --from-literal=api-secret-key=$(openssl rand -hex 32) \
  --dry-run=client -o yaml | kubectl apply -f -
```

### 4. Set up your domain (optional)

Update `k8s/ingress.yaml` with your actual domain, then:

```bash
kubectl apply -f k8s/ingress.yaml
```

Or use the Civo-provided DNS entry:

```bash
cd terraform && terraform output dns_entry
```

## Operations

### Check status
```bash
./deploy.sh status
```

### Destroy everything (stops all charges)
```bash
./deploy.sh destroy
```

### Rebuild and redeploy just the app
```bash
./deploy.sh docker   # rebuild image
./deploy.sh k8s      # reapply k8s manifests
```

## API Endpoints

| Method | Path       | Description                        |
|--------|------------|------------------------------------|
| POST   | /dispatch  | Execute code via sovereign dispatch|
| GET    | /budget    | Current budget status              |
| GET    | /runtime   | Runtime environment info           |
| GET    | /healthz   | Health check                       |

### Example: dispatch code

```bash
curl -X POST https://your-domain/dispatch \
  -H "Authorization: Bearer YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(40 + 2)", "kind": "python"}'
```

## File Structure

```
infrastructure/civo/
  terraform/
    providers.tf    - Civo provider configuration
    variables.tf    - Input variables with defaults
    main.tf         - Network, firewall, k8s cluster
    outputs.tf      - Cluster endpoint, kubeconfig path
  k8s/
    namespace.yaml  - tardis-sovereign namespace
    configmap.yaml  - Dispatch configuration (from default.yaml)
    secrets.yaml    - API keys (TEMPLATE - edit before use)
    deployment.yaml - Dispatch API deployment (1 replica)
    service.yaml    - ClusterIP service
    ingress.yaml    - Traefik ingress with TLS
  Dockerfile        - Multi-stage Python build
  serve.py          - Minimal HTTP API wrapper (stdlib only)
  deploy.sh         - One-command deployment script
  README.md         - This file
```

## UK Sovereignty

All data stays in Civo's LON1 (London) data centre. Civo is a UK-based
cloud provider. No data transits through non-UK infrastructure when using
LON1 region exclusively.
