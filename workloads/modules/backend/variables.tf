variable "namespace" {
  description = "Namespace to deploy the backend into."
  type        = string
}

variable "vertex_project" {
  description = "GCP project hosting Vertex AI Gemini."
  type        = string
}

variable "vertex_region" {
  description = "Vertex AI region."
  type        = string
}

variable "db_host" {
  description = "Postgres host."
  type        = string
}

variable "db_port" {
  description = "Postgres port."
  type        = string
}

variable "db_name" {
  description = "Postgres database name."
  type        = string
}

variable "db_user" {
  description = "Postgres user."
  type        = string
}
