terraform {
  required_version = ">= 1.6"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.27"
    }
  }

  # PLACEHOLDER: Doctor must provision the Terraform Cloud workspace
  # "tardis-workloads" under the <doctor-org> organisation and substitute
  # the organisation name below before the first `terraform init`.
  # Phase 4 wires this live.
  cloud {
    organization = "PLACEHOLDER_TF_CLOUD_ORG"
    workspaces {
      name = "tardis-workloads"
    }
  }
}

# PLACEHOLDER kubernetes provider config.
# Phase 4 replaces this with a data "terraform_remote_state" "cluster"
# block reading the cluster module's outputs from its own TF Cloud workspace
# (tardis-sovereign-cluster) and wires host/ca/token from there.
provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "tardis-sovereign"
}
