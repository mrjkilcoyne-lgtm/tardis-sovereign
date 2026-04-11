variable "image_tag" {
  description = "Container image tag for tardis-backend (pulled from GHCR)."
  type        = string
  default     = "v0.0.1-placeholder"
}

variable "vertex_project" {
  description = "GCP project hosting Vertex AI Gemini."
  type        = string
  default     = "time-to-fix-thing-up"
}

variable "vertex_region" {
  description = "Vertex AI region."
  type        = string
  default     = "us-central1"
}

variable "db_host" {
  description = "Postgres host reachable from the tardis namespace."
  type        = string
  default     = "postgres.postgres.svc.cluster.local"
}

variable "db_port" {
  description = "Postgres port."
  type        = string
  default     = "5432"
}

variable "db_name" {
  description = "Postgres database name."
  type        = string
  default     = "tardis"
}

variable "db_user" {
  description = "Postgres user."
  type        = string
  default     = "tardis_admin"
}

variable "namespace" {
  description = "Kubernetes namespace for TARDIS workloads."
  type        = string
  default     = "tardis"
}
