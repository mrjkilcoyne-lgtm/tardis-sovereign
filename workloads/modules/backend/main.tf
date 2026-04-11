# Phase 3 scaffold: SA, RBAC, ConfigMap, and ClusterIP Service.
# Phase 4 adds the Deployment once the Layer 2 image lands in GHCR
# (sketched in design doc §4.5).

resource "kubernetes_config_map" "tardis_backend" {
  metadata {
    name      = "tardis-backend-config"
    namespace = var.namespace
  }
  data = {
    VERTEX_PROJECT     = var.vertex_project
    VERTEX_REGION      = var.vertex_region
    VERTEX_MODEL       = "gemini-2.5-pro"
    VERTEX_EMBED_MODEL = "text-embedding-005"
    DB_HOST            = var.db_host
    DB_PORT            = var.db_port
    DB_NAME            = var.db_name
    DB_USER            = var.db_user
    GITEA_BASE_URL     = "http://gitea.tardis.svc.cluster.local:3000"
    LOG_LEVEL          = "info"
    PORT               = "8080"
  }
}

resource "kubernetes_service_account" "tardis_backend" {
  metadata {
    name      = "tardis-backend"
    namespace = var.namespace
  }
  automount_service_account_token = false
}

resource "kubernetes_role" "tardis_backend" {
  metadata {
    name      = "tardis-backend"
    namespace = var.namespace
  }
  rule {
    api_groups     = [""]
    resources      = ["secrets", "configmaps"]
    resource_names = ["tardis-backend-secrets", "tardis-backend-config"]
    verbs          = ["get"]
  }
}

resource "kubernetes_role_binding" "tardis_backend" {
  metadata {
    name      = "tardis-backend"
    namespace = var.namespace
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.tardis_backend.metadata[0].name
  }
  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.tardis_backend.metadata[0].name
    namespace = var.namespace
  }
}

resource "kubernetes_service" "tardis_backend" {
  metadata {
    name      = "tardis-backend"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "tardis-backend"
    }
    type = "ClusterIP"
    port {
      port        = 8080
      target_port = 8080
      protocol    = "TCP"
    }
  }
}
