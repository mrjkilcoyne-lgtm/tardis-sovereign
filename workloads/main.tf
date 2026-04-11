module "namespace" {
  source = "./modules/namespace"

  namespace = var.namespace
}

module "secrets" {
  source = "./modules/secrets"

  namespace = module.namespace.name
}

module "backend" {
  source = "./modules/backend"

  namespace      = module.namespace.name
  vertex_project = var.vertex_project
  vertex_region  = var.vertex_region
  db_host        = var.db_host
  db_port        = var.db_port
  db_name        = var.db_name
  db_user        = var.db_user

  depends_on = [module.secrets]
}

module "network_policy" {
  source = "./modules/network-policy"

  namespace = module.namespace.name
}

module "tailscale_ingress" {
  source = "./modules/tailscale-ingress"

  namespace = module.namespace.name

  depends_on = [module.backend]
}
