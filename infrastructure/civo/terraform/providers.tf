terraform {
  required_version = ">= 1.5.0"

  required_providers {
    civo = {
      source  = "civo/civo"
      version = "~> 1.0"
    }
  }
}

provider "civo" {
  token  = var.civo_token
  region = var.region
}
