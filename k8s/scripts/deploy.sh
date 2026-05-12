#!/bin/bash
# =============================================================
# TARDIS Sovereign — Full Stack Deployment Script
# =============================================================
# Usage: ./deploy.sh [phase]
#   phase 1 — Core infrastructure (namespaces, cert-manager, DB, cache)
#   phase 2 — Monitoring (Prometheus, Grafana)
#   phase 3 — AI services (LGM, Luggage)
#   phase 4 — Revenue apps (ClaimourLife, Hex, BAKK, etc.)
#   all     — Everything in order
# =============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="$(dirname "$SCRIPT_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[TARDIS]${NC} $1"; }
warn() { echo -e "${YELLOW}[TARDIS]${NC} $1"; }
err()  { echo -e "${RED}[TARDIS]${NC} $1"; }

check_prereqs() {
    log "Checking prerequisites..."
    command -v kubectl >/dev/null 2>&1 || { err "kubectl not found. Install it first."; exit 1; }
    command -v helm >/dev/null 2>&1 || { err "helm not found. Install it first."; exit 1; }

    if ! kubectl cluster-info >/dev/null 2>&1; then
        err "Cannot connect to cluster. Set KUBECONFIG or check your connection."
        err "  export KUBECONFIG=\$(terraform output -raw kubeconfig)"
        exit 1
    fi
    log "Connected to cluster: $(kubectl config current-context)"
}

phase1_core() {
    log "=== PHASE 1: Core Infrastructure ==="

    log "Creating namespaces..."
    kubectl apply -f "$K8S_DIR/core/namespaces.yaml"

    log "Installing cert-manager via Helm..."
    helm repo add jetstack https://charts.jetstack.io 2>/dev/null || true
    helm repo update
    helm upgrade --install cert-manager jetstack/cert-manager \
        --namespace cert-manager \
        --create-namespace \
        --set crds.enabled=true \
        --wait

    log "Applying Let's Encrypt issuers..."
    kubectl apply -f "$K8S_DIR/core/cert-manager-issuers.yaml"

    warn "IMPORTANT: Edit postgres-credentials secret before deploying!"
    warn "  kubectl -n tardis-core edit secret postgres-credentials"
    log "Deploying PostgreSQL..."
    kubectl apply -f "$K8S_DIR/core/postgres.yaml"

    log "Deploying Redis..."
    kubectl apply -f "$K8S_DIR/core/redis.yaml"

    log "Waiting for core services..."
    kubectl -n tardis-core wait --for=condition=ready pod -l app=postgres --timeout=120s
    kubectl -n tardis-core wait --for=condition=ready pod -l app=redis --timeout=60s

    log "Phase 1 complete. Core infrastructure is running."
}

phase2_monitoring() {
    log "=== PHASE 2: Monitoring ==="

    log "Deploying Prometheus + Grafana..."
    kubectl apply -f "$K8S_DIR/monitoring/prometheus-grafana.yaml"

    log "Waiting for monitoring services..."
    kubectl -n tardis-monitoring wait --for=condition=ready pod -l app=prometheus --timeout=120s
    kubectl -n tardis-monitoring wait --for=condition=ready pod -l app=grafana --timeout=60s

    warn "IMPORTANT: Change Grafana admin password!"
    warn "  Default: admin / CHANGE_ME_BEFORE_DEPLOY"
    log "Phase 2 complete. Monitoring is running."
}

phase3_ai() {
    log "=== PHASE 3: AI Services ==="

    log "Deploying LGM API..."
    kubectl apply -f "$K8S_DIR/apps/lgm-api.yaml"

    log "Deploying The Luggage..."
    kubectl apply -f "$K8S_DIR/apps/luggage.yaml"

    log "Waiting for AI services..."
    kubectl -n tardis-ai wait --for=condition=ready pod -l app=lgm-api --timeout=180s
    kubectl -n tardis-ai wait --for=condition=ready pod -l app=luggage --timeout=120s

    log "Phase 3 complete. AI services are running."
}

phase4_apps() {
    log "=== PHASE 4: Revenue Apps ==="

    log "Deploying ClaimourLife..."
    kubectl apply -f "$K8S_DIR/apps/claimourlife.yaml"

    log "Deploying Hex Inventions..."
    kubectl apply -f "$K8S_DIR/apps/hex-inventions.yaml"

    log "Deploying BAKK Online..."
    kubectl apply -f "$K8S_DIR/apps/bakk-online.yaml"

    log "Waiting for apps..."
    kubectl -n tardis-apps wait --for=condition=ready pod -l app=claimourlife --timeout=120s
    kubectl -n tardis-apps wait --for=condition=ready pod -l app=hex-inventions --timeout=120s
    kubectl -n tardis-apps wait --for=condition=ready pod -l app=bakk-online --timeout=120s

    log "Phase 4 complete. Revenue apps are running."
}

status() {
    log "=== TARDIS Sovereign Status ==="
    echo ""
    echo "--- Namespaces ---"
    kubectl get ns | grep tardis
    echo ""
    echo "--- Core Services ---"
    kubectl -n tardis-core get pods 2>/dev/null || echo "  (not deployed)"
    echo ""
    echo "--- Monitoring ---"
    kubectl -n tardis-monitoring get pods 2>/dev/null || echo "  (not deployed)"
    echo ""
    echo "--- AI Services ---"
    kubectl -n tardis-ai get pods 2>/dev/null || echo "  (not deployed)"
    echo ""
    echo "--- Apps ---"
    kubectl -n tardis-apps get pods 2>/dev/null || echo "  (not deployed)"
    echo ""
    echo "--- Ingresses ---"
    kubectl get ingress --all-namespaces 2>/dev/null || echo "  (none)"
}

case "${1:-}" in
    1|phase1|core)      check_prereqs; phase1_core ;;
    2|phase2|monitoring) check_prereqs; phase2_monitoring ;;
    3|phase3|ai)        check_prereqs; phase3_ai ;;
    4|phase4|apps)      check_prereqs; phase4_apps ;;
    all)
        check_prereqs
        phase1_core
        phase2_monitoring
        phase3_ai
        phase4_apps
        log "=== ALL PHASES COMPLETE ==="
        status
        ;;
    status)             check_prereqs; status ;;
    *)
        echo "TARDIS Sovereign Deployment"
        echo ""
        echo "Usage: $0 {1|2|3|4|all|status}"
        echo ""
        echo "Phases:"
        echo "  1 (core)       — Namespaces, cert-manager, PostgreSQL, Redis"
        echo "  2 (monitoring) — Prometheus, Grafana"
        echo "  3 (ai)         — LGM API, The Luggage"
        echo "  4 (apps)       — ClaimourLife, Hex Inventions, BAKK Online"
        echo "  all            — Deploy everything in order"
        echo "  status         — Show cluster status"
        ;;
esac
