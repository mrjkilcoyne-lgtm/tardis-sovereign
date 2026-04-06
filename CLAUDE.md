# CLAUDE.md

## Project Overview

**tardis-sovereign** is the infrastructure backbone for the TARDIS Sovereign AI ecosystem. It provisions a K3s Kubernetes cluster on [Civo Cloud](https://www.civo.com/) (LON1 region) and contains all Kubernetes manifests, deployment scripts, and CI/CD pipelines for the full application stack.

## Repository Structure

```
.
├── main.tf                          # Civo provider, network lookup, firewall, K3s cluster
├── variables.tf                     # Input variables (civo_token, cluster_name, region, node_count)
├── outputs.tf                       # Outputs: cluster_id, kubeconfig (sensitive)
├── terraform.tf                     # Terraform version & provider version constraints
├── THE_PLAN.md                      # Full ecosystem strategy and bootstrapper's guide
├── Dockerfile.template              # Node.js/TypeScript app Dockerfile template
├── Dockerfile.static                # Static site (Eleventy/Astro) Dockerfile template
├── Dockerfile.python                # Python service (LGM/Luggage) Dockerfile template
├── k8s/
│   ├── core/
│   │   ├── namespaces.yaml          # tardis-core, tardis-apps, tardis-ai, tardis-monitoring
│   │   ├── cert-manager-issuers.yaml # Let's Encrypt prod + staging via Traefik
│   │   ├── postgres.yaml            # PostgreSQL 16 — shared DB for all apps
│   │   └── redis.yaml               # Redis 7 — caching and message queue
│   ├── apps/
│   │   ├── app-template.yaml        # Generic app deployment template (copy & fill)
│   │   ├── claimourlife.yaml        # ClaimourLife static site
│   │   ├── hex-inventions.yaml      # Hex Inventions (IGOR Protocol pipeline)
│   │   ├── bakk-online.yaml         # BAKK Online (CANZUK social platform)
│   │   ├── lgm-api.yaml             # LGM — Large Grammar Model API
│   │   └── luggage.yaml             # The Luggage — AI agent orchestration
│   ├── monitoring/
│   │   └── prometheus-grafana.yaml  # Prometheus + Grafana monitoring stack
│   └── scripts/
│       ├── deploy.sh                # Phased deployment script (core → monitoring → AI → apps)
│       ├── setup-kubeconfig.sh      # Extract kubeconfig from Terraform
│       └── tailscale-join.sh        # Install Tailscale VPN mesh on cluster
└── .github/
    └── workflows/
        ├── terraform.yml            # Terraform: fmt check, plan on PRs; apply on push to main
        ├── deploy-k8s.yml           # K8s: deploy manifests (manual or on k8s/ changes)
        └── build-images.yml         # Build & push container images to GHCR
```

## Key Technologies

- **Terraform** >= 1.0 (IaC for Civo Cloud)
- **Civo provider** ~> 1.1 (`civo/civo`)
- **Kubernetes**: K3s cluster, `g4s.kube.small` node size, default 1 worker node
- **Traefik**: Ingress controller (included with K3s)
- **cert-manager**: Automatic TLS via Let's Encrypt
- **PostgreSQL 16**: Shared database
- **Redis 7**: Caching and queues
- **Prometheus + Grafana**: Monitoring
- **Tailscale**: Mesh VPN connecting cluster, phone, and home server
- **GitHub Actions**: CI/CD (Terraform, K8s deploys, container builds)
- **GHCR**: Container image registry (ghcr.io/mrjkilcoyne-lgtm/*)

## Kubernetes Namespaces

| Namespace | Purpose |
|-----------|---------|
| `tardis-core` | PostgreSQL, Redis, shared infrastructure |
| `tardis-apps` | Revenue apps (ClaimourLife, Hex, BAKK, etc.) |
| `tardis-ai` | LGM API, The Luggage agent platform |
| `tardis-monitoring` | Prometheus, Grafana |

## Development Workflow

### Local Development (Terraform)

1. Set the `CIVO_TOKEN` environment variable or pass `civo_token` via a `.tfvars` file.
2. Run `terraform init` to initialize providers.
3. Run `terraform fmt` to format files (CI enforces this).
4. Run `terraform plan` to preview changes.
5. Run `terraform apply` to apply (only do this if you intend to modify live infrastructure).

### Deploying to the Cluster

1. Extract kubeconfig: `./k8s/scripts/setup-kubeconfig.sh`
2. Deploy by phase: `./k8s/scripts/deploy.sh {1|2|3|4|all}`
   - Phase 1: Core (namespaces, cert-manager, PostgreSQL, Redis)
   - Phase 2: Monitoring (Prometheus, Grafana)
   - Phase 3: AI (LGM API, The Luggage)
   - Phase 4: Apps (ClaimourLife, Hex Inventions, BAKK Online)
3. Check status: `./k8s/scripts/deploy.sh status`

### Adding a New App

1. Copy `k8s/apps/app-template.yaml`
2. Replace all `{{PLACEHOLDERS}}` with your app's values
3. Copy the appropriate `Dockerfile.*` template to your app repo
4. Build image: trigger `build-images.yml` workflow with app name and repo
5. Apply manifest: `kubectl apply -f k8s/apps/your-app.yaml`

### CI/CD Pipelines

| Workflow | Trigger | Action |
|----------|---------|--------|
| `terraform.yml` | PR: plan; push to main: apply | Provisions Civo K3s cluster |
| `deploy-k8s.yml` | Push to main (k8s/ changes) or manual | Deploys K8s manifests |
| `build-images.yml` | Manual dispatch | Builds & pushes container images to GHCR |

### Required GitHub Secrets

| Secret | Where | Purpose |
|--------|-------|---------|
| `CIVO_TOKEN` | production environment | Civo API authentication |
| `KUBECONFIG` | production environment | kubectl cluster access |
| `GH_PAT` | repository secret | Cross-repo image builds |

## Conventions

- **Formatting**: All `.tf` files must pass `terraform fmt -check`. Always run `terraform fmt` before committing.
- **Sensitive values**: `civo_token` and `kubeconfig` are marked `sensitive`. Never commit secrets or tokens.
- **Naming**: Terraform resources use `${var.cluster_name}-` prefix. K8s resources use `tardis-` namespace prefix.
- **Defaults**: `cluster_name = "tardis-sovereign"`, `region = "LON1"`, `node_count = 1`.
- **Images**: All container images go to `ghcr.io/mrjkilcoyne-lgtm/<app-name>`.
- **Secrets in K8s**: Use Kubernetes Secrets — NEVER hardcode credentials in manifests. The placeholder `CHANGE_ME_BEFORE_DEPLOY` marks values that must be changed.

## The TARDIS Ecosystem

This cluster hosts the full stack:

- **LGM** (Large Grammar Model) — cloud AI brain (Python)
- **The Luggage** — autonomous AI agent platform, MCP-native (Python)
- **MKAngel/GLM** — on-device Grammar Language Model (~370K params, runs on Android, NOT on this cluster)
- **Hex Inventions** — IGOR Protocol agent swarm, daily invention teardowns
- **InventorForge** — invention-to-patent pipeline
- **ClaimourLife** — 1300+ digital life reclaiming spells
- **BAKK Online** — CANZUK social infrastructure (£10/mo premium tier)
- **+ more** — see THE_PLAN.md for the full ecosystem map

## Important Notes for AI Assistants

- This repo manages **live cloud infrastructure**. Any changes to `.tf` files merged to `main` will be automatically applied. Treat all Terraform changes as high-impact.
- K8s manifest changes to `main` will also auto-deploy. Review carefully.
- Do not add or modify provider credentials in code. Secrets are managed via GitHub Actions environment secrets.
- The network data source (`civo_network.default`) looks up the default network by label — do not hardcode network IDs.
- The firewall uses `create_default_rules = true`; custom rules should be added carefully.
- When adding new resources, follow the existing pattern: Terraform in root `.tf` files, K8s manifests in `k8s/`, apps in `k8s/apps/`.
- Always change `CHANGE_ME_BEFORE_DEPLOY` placeholder passwords before deploying.
