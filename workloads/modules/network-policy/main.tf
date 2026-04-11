resource "kubernetes_network_policy" "default_deny_all" {
  metadata {
    name      = "default-deny-all"
    namespace = var.namespace
  }
  spec {
    pod_selector {}
    policy_types = ["Ingress", "Egress"]
  }
}

resource "kubernetes_network_policy" "tardis_backend_allow" {
  metadata {
    name      = "tardis-backend-allow"
    namespace = var.namespace
  }
  spec {
    pod_selector {
      match_labels = {
        app = "tardis-backend"
      }
    }
    policy_types = ["Ingress", "Egress"]

    ingress {
      from {
        namespace_selector {
          match_labels = {
            "kubernetes.io/metadata.name" = "tailscale"
          }
        }
      }
      ports {
        port     = "8080"
        protocol = "TCP"
      }
    }

    # Postgres egress
    egress {
      to {
        namespace_selector {
          match_labels = {
            "kubernetes.io/metadata.name" = "postgres"
          }
        }
      }
      ports {
        port     = "5432"
        protocol = "TCP"
      }
    }

    # Gitea egress (same namespace, pod selector)
    egress {
      to {
        pod_selector {
          match_labels = {
            app = "gitea"
          }
        }
      }
      ports {
        port     = "3000"
        protocol = "TCP"
      }
      ports {
        port     = "22"
        protocol = "TCP"
      }
    }

    # Vertex AI HTTPS (external, non-RFC1918)
    egress {
      to {
        ip_block {
          cidr = "0.0.0.0/0"
          except = [
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
          ]
        }
      }
      ports {
        port     = "443"
        protocol = "TCP"
      }
    }

    # kube-dns
    egress {
      to {
        namespace_selector {
          match_labels = {
            "kubernetes.io/metadata.name" = "kube-system"
          }
        }
      }
      ports {
        port     = "53"
        protocol = "UDP"
      }
      ports {
        port     = "53"
        protocol = "TCP"
      }
    }
  }
}
