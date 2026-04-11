# Tailscale operator is assumed installed out-of-band (design doc §4.7).
# This Ingress is picked up by the operator and published as
# https://tardis-backend.<tailnet>.ts.net — no public IP, no public DNS.
resource "kubernetes_manifest" "tardis_tailscale_ingress" {
  manifest = {
    apiVersion = "networking.k8s.io/v1"
    kind       = "Ingress"
    metadata = {
      name      = "tardis-backend"
      namespace = var.namespace
    }
    spec = {
      ingressClassName = "tailscale"
      rules = [{
        host = "tardis-backend"
        http = {
          paths = [{
            path     = "/"
            pathType = "Prefix"
            backend = {
              service = {
                name = "tardis-backend"
                port = {
                  number = 8080
                }
              }
            }
          }]
        }
      }]
      tls = [{
        hosts = ["tardis-backend"]
      }]
    }
  }
}
