#!/usr/bin/env bash
# =============================================================================
# TARDIS Sovereign - One-command Civo deployment
# Usage: ./deploy.sh [apply|destroy|status]
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TF_DIR="${SCRIPT_DIR}/terraform"
K8S_DIR="${SCRIPT_DIR}/k8s"
KUBECONFIG_PATH="${SCRIPT_DIR}/kubeconfig"
IMAGE_NAME="sovereign-dispatch"
IMAGE_TAG="latest"

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[TARDIS]${NC} $*"; }
warn() { echo -e "${YELLOW}[TARDIS]${NC} $*"; }
err()  { echo -e "${RED}[TARDIS]${NC} $*" >&2; }

# --- Pre-flight checks ---
preflight() {
    local missing=0
    for cmd in terraform kubectl docker; do
        if ! command -v "$cmd" &>/dev/null; then
            err "Required tool not found: $cmd"
            missing=1
        fi
    done
    if [[ -z "${TF_VAR_civo_token:-}" ]]; then
        err "TF_VAR_civo_token environment variable is not set."
        err "Get your API key from: https://dashboard.civo.com/security"
        err "Export it:  export TF_VAR_civo_token=YOUR_API_KEY"
        exit 1
    fi
    if [[ $missing -eq 1 ]]; then
        exit 1
    fi
    log "Pre-flight checks passed."
}

# --- Terraform: provision infrastructure ---
tf_apply() {
    log "Provisioning Civo infrastructure (LON1, UK sovereign)..."
    cd "$TF_DIR"
    terraform init -input=false
    terraform plan -out=tfplan -input=false
    terraform apply -input=false tfplan
    rm -f tfplan
    cd "$SCRIPT_DIR"
    log "Infrastructure provisioned."
}

tf_destroy() {
    warn "Destroying Civo infrastructure..."
    cd "$TF_DIR"
    terraform init -input=false
    terraform destroy -auto-approve
    cd "$SCRIPT_DIR"
    rm -f "$KUBECONFIG_PATH"
    log "Infrastructure destroyed."
}

tf_status() {
    cd "$TF_DIR"
    if terraform state list &>/dev/null 2>&1; then
        terraform output
    else
        warn "No Terraform state found. Infrastructure not provisioned."
    fi
    cd "$SCRIPT_DIR"
}

# --- Docker: build the image ---
docker_build() {
    log "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
    docker build \
        -t "${IMAGE_NAME}:${IMAGE_TAG}" \
        -f "${SCRIPT_DIR}/Dockerfile" \
        "${REPO_ROOT}"
    log "Docker image built."
}

# --- Kubernetes: deploy the application ---
k8s_apply() {
    if [[ ! -f "$KUBECONFIG_PATH" ]]; then
        err "Kubeconfig not found at ${KUBECONFIG_PATH}"
        err "Run './deploy.sh apply' to provision infrastructure first."
        exit 1
    fi

    export KUBECONFIG="$KUBECONFIG_PATH"
    log "Deploying to Kubernetes..."

    # Apply in order: namespace first, then config, then workloads
    kubectl apply -f "${K8S_DIR}/namespace.yaml"
    kubectl apply -f "${K8S_DIR}/configmap.yaml"

    # Check if secrets have been customised
    if grep -q "PLACEHOLDER_REPLACE" "${K8S_DIR}/secrets.yaml"; then
        warn "secrets.yaml still contains PLACEHOLDER values."
        warn "Edit ${K8S_DIR}/secrets.yaml before production use,"
        warn "or create secrets via kubectl:"
        warn "  kubectl create secret generic sovereign-dispatch-secrets \\"
        warn "    --namespace=tardis-sovereign \\"
        warn "    --from-literal=civo-api-key=YOUR_KEY \\"
        warn "    --from-literal=api-secret-key=YOUR_SECRET"
        warn ""
        warn "Applying template secrets for now (NOT production-safe)..."
    fi
    kubectl apply -f "${K8S_DIR}/secrets.yaml"

    kubectl apply -f "${K8S_DIR}/deployment.yaml"
    kubectl apply -f "${K8S_DIR}/service.yaml"
    kubectl apply -f "${K8S_DIR}/ingress.yaml"

    log "Kubernetes resources applied."
    log ""
    log "Waiting for deployment to be ready..."
    kubectl -n tardis-sovereign rollout status deployment/sovereign-dispatch --timeout=120s || true
    log ""
    log "Cluster info:"
    kubectl -n tardis-sovereign get pods,svc,ingress
}

# --- Main ---
ACTION="${1:-apply}"

case "$ACTION" in
    apply)
        preflight
        tf_apply
        docker_build
        k8s_apply
        log ""
        log "Deployment complete. Estimated cost: ~GBP 20/month."
        log "Your GBP 250 credits should last ~12 months."
        ;;
    destroy)
        preflight
        tf_destroy
        log "All resources destroyed. No further charges."
        ;;
    status)
        tf_status
        if [[ -f "$KUBECONFIG_PATH" ]]; then
            export KUBECONFIG="$KUBECONFIG_PATH"
            echo ""
            log "Kubernetes resources:"
            kubectl -n tardis-sovereign get pods,svc,ingress 2>/dev/null || warn "Cluster not reachable."
        fi
        ;;
    docker)
        docker_build
        ;;
    k8s)
        k8s_apply
        ;;
    *)
        echo "Usage: $0 [apply|destroy|status|docker|k8s]"
        echo ""
        echo "  apply   - Full deploy: terraform + docker build + kubectl apply"
        echo "  destroy - Tear down all Civo infrastructure"
        echo "  status  - Show current infrastructure and pod status"
        echo "  docker  - Build Docker image only"
        echo "  k8s     - Apply Kubernetes manifests only (cluster must exist)"
        exit 1
        ;;
esac
