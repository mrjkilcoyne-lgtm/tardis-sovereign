variable "civo_token" {
  description = "Civo API token. Set via TF_VAR_civo_token or -var."
  type        = string
  sensitive   = true
}

variable "cluster_name" {
  description = "Name of the Kubernetes cluster"
  type        = string
  default     = "tardis-sovereign"
}

variable "region" {
  description = "Civo region. LON1 = UK sovereign."
  type        = string
  default     = "LON1"
}

variable "node_size" {
  description = "Node instance size. g4s.kube.small = cheapest option."
  type        = string
  default     = "g4s.kube.small"
}

variable "node_count" {
  description = "Number of worker nodes. 2 = minimal HA."
  type        = number
  default     = 2
}

variable "kubernetes_version" {
  description = "Kubernetes version to deploy"
  type        = string
  default     = "1.28.2-k3s1"
}

variable "cluster_type" {
  description = "Cluster type: k3s (cheaper) or talos"
  type        = string
  default     = "k3s"
}

variable "domain" {
  description = "Domain for ingress. Set to your domain or use Civo DNS."
  type        = string
  default     = "tardis-sovereign.example.com"
}
