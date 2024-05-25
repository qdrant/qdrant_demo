terraform {
  required_version = ">= 1.7.5"

  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.13.2"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}