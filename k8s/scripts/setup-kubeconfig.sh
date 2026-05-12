#!/bin/bash
# =============================================================
# Extract kubeconfig from Terraform and configure kubectl
# =============================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "[TARDIS] Extracting kubeconfig from Terraform..."
cd "$REPO_ROOT"

if ! command -v terraform >/dev/null 2>&1; then
    echo "[ERROR] terraform not found. Install it first."
    exit 1
fi

terraform output -raw kubeconfig > ~/.kube/tardis-sovereign.yaml
chmod 600 ~/.kube/tardis-sovereign.yaml
export KUBECONFIG=~/.kube/tardis-sovereign.yaml

echo "[TARDIS] kubeconfig saved to ~/.kube/tardis-sovereign.yaml"
echo "[TARDIS] Run: export KUBECONFIG=~/.kube/tardis-sovereign.yaml"
echo ""
echo "[TARDIS] Testing connection..."
kubectl cluster-info
echo ""
echo "[TARDIS] Nodes:"
kubectl get nodes
