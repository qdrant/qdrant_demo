
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

resource "google_compute_network" "vpc" {
  name                    = "neural-search-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "neural-search-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.gcp_region
  network       = google_compute_network.vpc.name
}

resource "google_container_cluster" "gke" {
  name     = "neural-search-gke"
  location = var.gcp_region

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  initial_node_count = 1

  node_config {
    machine_type = "e2-medium"
  }
}

# Export kubeconfig for Helm provider
resource "local_file" "kubeconfig" {
  content  = google_container_cluster.gke.kube_config_raw
  filename = "${path.module}/kubeconfig_gcp"
}
