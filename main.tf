provider "civo" {
  token  = var.civo_token
  region = var.region
}

# Firewall for the Kubernetes cluster
resource "civo_firewall" "tardis_firewall" {
  name                 = "${var.cluster_name}-firewall"
  network_id           = "default"
  create_default_rules = true
}

# Kubernetes cluster on Civo (K3s)
resource "civo_kubernetes_cluster" "tardis" {
  name         = var.cluster_name
  region       = var.region
  firewall_id  = civo_firewall.tardis_firewall.id
  cluster_type = "k3s"

  pools {
    size       = "g4s.kube.small"
    node_count = var.node_count
  }
}
