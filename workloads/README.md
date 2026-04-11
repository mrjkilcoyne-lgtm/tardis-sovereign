# TARDIS Workloads — Manual Apply Runbook

This Terraform root provisions the TARDIS backend workload on the existing
`tardis-sovereign` K3s cluster. **CI never applies these.** Apply is always
manual from Matt's workstation.

## State

Separate from the cluster module. State lives in Terraform Cloud workspace
`tardis-workloads` under the `<doctor-org>` organisation (currently a
`PLACEHOLDER_TF_CLOUD_ORG` in `terraform.tf` — Doctor must provision the
workspace and substitute before first apply).

## Prerequisites

- `terraform` >= 1.6
- `kubectl` with `KUBECONFIG` pointing at the `tardis-sovereign` cluster
- `sops` installed (Phase 4, once SOPS-encrypted secrets replace the
  placeholder `kubernetes_secret` values)
- Age private key at `~/.config/sops/age/keys.txt` (Phase 4)
- `TF_TOKEN_app_terraform_io` environment variable for Terraform Cloud

## Step 1 — Verify cluster reachable

```bash
kubectl get nodes
```

## Step 2 — Navigate

```bash
cd tardis-sovereign/workloads
```

## Step 3 — Init (after provider changes only)

```bash
terraform init
```

## Step 4 — Plan

```bash
terraform plan -out=tardis.tfplan
```

## Step 5 — REVIEW

- Confirm only `tardis` namespace resources change
- Confirm no cluster-level resources are in scope
- Confirm `image_tag` matches the intended GHCR tag

## Step 6 — Apply

```bash
terraform apply tardis.tfplan
```

## Step 7 — Verify

```bash
kubectl -n tardis get pods
kubectl -n tardis get ingress
kubectl -n tardis logs -l app=tardis-backend --tail=50
```

## Step 8 — Smoke test from phone

Open the TARDIS app and confirm `tardis-backend.<tailnet>.ts.net` responds.

## Rollback

```bash
terraform apply -var="image_tag=<previous_tag>"
```

## Scope

- IN: `tardis` namespace, ConfigMap, SA, RBAC, Service, NetworkPolicy,
  Tailscale Ingress, placeholder Secret.
- OUT: Deployment (Phase 4, once Layer 2 image is in GHCR), Tailscale
  operator install (manual one-time Helm), cluster provisioning (separate
  root module), Postgres (pre-existing), Gitea manifests (plain YAML in
  `k8s/tardis/gitea/`).

## CI

`.github/workflows/workloads-plan.yml` runs `terraform fmt -check`,
`terraform validate`, and `terraform plan` on PRs that touch
`workloads/**`. **There is no `terraform apply` step. Ever.**
