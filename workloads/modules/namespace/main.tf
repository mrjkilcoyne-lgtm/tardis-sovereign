resource "kubernetes_namespace" "tardis" {
  metadata {
    name = var.namespace
    labels = {
      "app.kubernetes.io/part-of" = "tardis"
      "purpose"                   = "vessel-console"
    }
  }
}
