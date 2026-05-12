# -----------------------------------------------------------------------------
# TARDIS Sovereign - Civo Cloud Infrastructure
# UK-sovereign Kubernetes deployment (LON1 region)
# Designed for cost efficiency: ~GBP 20/month
# -----------------------------------------------------------------------------

# --- Network ---
resource "civo_network" "sovereign" {
  label  = "${var.cluster_name}-network"
  region = var.region
}

# --- Firewall ---
resource "civo_firewall" "sovereign" {
  name                 = "${var.cluster_name}-fw"
  network_id           = civo_network.sovereign.id
  region               = var.region
  create_default_rules = false
}

resource "civo_firewall_rule" "https" {
  firewall_id = civo_firewall.sovereign.id
  protocol    = "tcp"
  start_port  = "443"
  end_port    = "443"
  cidr        = ["0.0.0.0/0"]
  direction   = "ingress"
  action      = "allow"
  label       = "Allow HTTPS"
  region      = var.region
}

resource "civo_firewall_rule" "http" {
  firewall_id = civo_firewall.sovereign.id
  protocol    = "tcp"
  start_port  = "80"
  end_port    = "80"
  cidr        = ["0.0.0.0/0"]
  direction   = "ingress"
  action      = "allow"
  label       = "Allow HTTP (redirect to HTTPS)"
  region      = var.region
}

resource "civo_firewall_rule" "kubernetes_api" {
  firewall_id = civo_firewall.sovereign.id
  protocol    = "tcp"
  start_port  = "6443"
  end_port    = "6443"
  cidr        = ["0.0.0.0/0"]
  direction   = "ingress"
  action      = "allow"
  label       = "Kubernetes API"
  region      = var.region
}

# --- Kubernetes Cluster ---
resource "civo_kubernetes_cluster" "sovereign" {
  name               = var.cluster_name
  region             = var.region
  cluster_type       = var.cluster_type
  kubernetes_version = var.kubernetes_version
  firewall_id        = civo_firewall.sovereign.id
  network_id         = civo_network.sovereign.id

  pools {
    label      = "${var.cluster_name}-pool"
    size       = var.node_size
    node_count = var.node_count
  }

  # Traefik is installed by default on Civo k3s clusters.
  # Only install what we actually need to save resources.
  applications = "Traefik-v2-nodeport"
}

# --- Write kubeconfig to local file ---
resource "local_file" "kubeconfig" {
  content              = civo_kubernetes_cluster.sovereign.kubeconfig
  filename             = "${path.module}/../kubeconfig"
  file_permission      = "0600"
  directory_permission = "0755"
}
