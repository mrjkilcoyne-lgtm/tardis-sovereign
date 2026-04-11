# PLACEHOLDER secrets.
# Phase 4 replaces the literal values below with a data "sops_file" "tardis"
# source decrypting workloads/secrets/tardis-secrets.enc.yaml at apply time
# with the Age key at ~/.config/sops/age/keys.txt.
#
# The keys here must match the keys referenced by the backend Deployment
# (db-password, phone-shared-secret, gitea-token, gcp-sa-key.json,
#  amendment-deploy-key) so the Deployment sketch in §4.5 of the design doc
# keeps lining up when live secrets land.
resource "kubernetes_secret" "tardis_backend_secrets" {
  metadata {
    name      = "tardis-backend-secrets"
    namespace = var.namespace
  }

  type = "Opaque"

  data = {
    "db-password"          = "PLACEHOLDER_DB_PASSWORD"
    "phone-shared-secret"  = "PLACEHOLDER_PHONE_SHARED_SECRET"
    "gitea-token"          = "PLACEHOLDER_GITEA_TOKEN"
    "gcp-sa-key.json"      = "PLACEHOLDER_GCP_SA_KEY_JSON"
    "amendment-deploy-key" = "PLACEHOLDER_AMENDMENT_DEPLOY_KEY"
    "gitea-admin-password" = "PLACEHOLDER_GITEA_ADMIN_PASSWORD"
  }
}
