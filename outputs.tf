output "cluster_id" {
  description = "ID of the Civo Kubernetes cluster"
  value       = civo_kubernetes_cluster.tardis.id
}

output "kubeconfig" {
  description = "Kubeconfig for the Civo Kubernetes cluster"
  value       = civo_kubernetes_cluster.tardis.kubeconfig
  sensitive   = true
}
