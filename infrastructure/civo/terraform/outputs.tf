output "cluster_id" {
  description = "Civo cluster ID"
  value       = civo_kubernetes_cluster.sovereign.id
}

output "cluster_endpoint" {
  description = "Kubernetes API endpoint"
  value       = civo_kubernetes_cluster.sovereign.api_endpoint
}

output "cluster_name" {
  description = "Cluster name"
  value       = civo_kubernetes_cluster.sovereign.name
}

output "kubeconfig_path" {
  description = "Path to the generated kubeconfig file"
  value       = local_file.kubeconfig.filename
}

output "dns_entry" {
  description = "Civo DNS name for the cluster"
  value       = civo_kubernetes_cluster.sovereign.dns_entry
}

output "master_ip" {
  description = "Master node IP address"
  value       = civo_kubernetes_cluster.sovereign.master_ip
}
