#!/bin/bash
# =============================================================
# Install Tailscale on the K3s cluster for mesh VPN
# Connects TARDIS cluster to your phone and home server
# =============================================================
set -euo pipefail

echo "[TARDIS] Installing Tailscale operator on K3s..."

helm repo add tailscale https://pkgs.tailscale.com/helmcharts 2>/dev/null || true
helm repo update

# You need a Tailscale auth key from https://login.tailscale.com/admin/settings/keys
if [ -z "${TS_AUTH_KEY:-}" ]; then
    echo ""
    echo "[TARDIS] You need a Tailscale auth key."
    echo "  1. Go to https://login.tailscale.com/admin/settings/keys"
    echo "  2. Generate an auth key (reusable, ephemeral)"
    echo "  3. Run: export TS_AUTH_KEY=tskey-auth-..."
    echo "  4. Re-run this script"
    exit 1
fi

kubectl create namespace tailscale --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic tailscale-auth \
    --namespace tailscale \
    --from-literal=TS_AUTHKEY="$TS_AUTH_KEY" \
    --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install tailscale-operator tailscale/tailscale-operator \
    --namespace tailscale \
    --set oauth.clientId="" \
    --set oauth.clientSecret="" \
    --wait

echo "[TARDIS] Tailscale operator installed."
echo "[TARDIS] Your cluster will appear in your Tailscale admin console."
echo "[TARDIS] Connect your phone and home server to the same Tailnet."
