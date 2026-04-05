# CLAUDE.md

## Project Overview

**tardis-sovereign** is a Terraform-based infrastructure project that provisions a K3s Kubernetes cluster on [Civo Cloud](https://www.civo.com/) in the LON1 region. It is the infrastructure backbone for the TARDIS Sovereign AI / LGM Server.

## Repository Structure

```
.
├── main.tf          # Core resources: Civo provider, network lookup, firewall, K3s cluster
├── variables.tf     # Input variables (civo_token, cluster_name, region, node_count)
├── outputs.tf       # Outputs: cluster_id, kubeconfig (sensitive)
├── terraform.tf     # Terraform version & provider version constraints
├── README.md
└── .github/
    └── workflows/
        └── terraform.yml   # CI/CD: fmt check, plan on PRs; apply on push to main
```

## Key Technologies

- **Terraform** >= 1.0 (IaC)
- **Civo provider** ~> 1.1 (`civo/civo`)
- **Kubernetes**: K3s cluster, `g4s.kube.small` node size, default 1 worker node
- **GitHub Actions**: CI/CD pipeline

## Development Workflow

### Local Development

1. Set the `CIVO_TOKEN` environment variable or pass `civo_token` via a `.tfvars` file.
2. Run `terraform init` to initialize providers.
3. Run `terraform fmt` to format files (CI enforces this).
4. Run `terraform plan` to preview changes.
5. Run `terraform apply` to apply (only do this if you intend to modify live infrastructure).

### CI/CD Pipeline (`.github/workflows/terraform.yml`)

- **On pull requests**: runs `terraform init`, `terraform fmt -check`, and `terraform plan`.
- **On push to `main`**: additionally runs `terraform apply -auto-approve`.
- The `CIVO_TOKEN` secret is injected via the `production` GitHub environment.

## Conventions

- **Formatting**: All `.tf` files must pass `terraform fmt -check`. Always run `terraform fmt` before committing.
- **Sensitive values**: The `civo_token` variable and `kubeconfig` output are marked `sensitive`. Never commit secrets or tokens.
- **Naming**: Resources use a `${var.cluster_name}-` prefix (e.g., `tardis-sovereign-firewall`).
- **Defaults**: `cluster_name = "tardis-sovereign"`, `region = "LON1"`, `node_count = 1`.

## Important Notes for AI Assistants

- This repo manages **live cloud infrastructure**. Any changes to `.tf` files merged to `main` will be automatically applied. Treat all Terraform changes as high-impact.
- Do not add or modify provider credentials in code. Secrets are managed via GitHub Actions environment secrets.
- The network data source (`civo_network.default`) looks up the default network by label — do not hardcode network IDs.
- The firewall uses `create_default_rules = true`; custom rules should be added carefully.
- When adding new resources, follow the existing pattern: define variables in `variables.tf`, resources in `main.tf`, and outputs in `outputs.tf`.
