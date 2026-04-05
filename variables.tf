variable "civo_token" {
  description = "Civo API token"
  type        = string
  sensitive   = true
}

variable "cluster_name" {
  description = "Name of the Kubernetes cluster"
  type        = string
  default     = "tardis-sovereign"
}

variable "region" {
  description = "Civo region to deploy into"
  type        = string
  default     = "LON1"
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 1
}
