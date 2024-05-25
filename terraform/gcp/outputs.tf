
output "vpc_name" {
  description = "The name of the VPC"
  value       = google_compute_network.vpc.name
}

output "gke_cluster_name" {
  description = "The name of the GKE cluster"
  value       = google_container_cluster.gke.name
}
