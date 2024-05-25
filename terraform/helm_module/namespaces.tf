resource "kubernetes_namespace" "qdrant-services" {
  metadata {
    annotations = {
      name = "qdrant-services"
    }

    labels = {
      istio-injection = "enabled"
    }

    name = "qdrant-services"
  }
}
resource "kubernetes_namespace" "istio-ingress" {
  metadata {
    annotations = {
      name = "istio-ingress"
    }

    labels = {
      istio-injection = "enabled"
    }

    name = "istio-ingress"
  }
}