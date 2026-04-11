output "name" {
  description = "Namespace name."
  value       = kubernetes_namespace.tardis.metadata[0].name
}
