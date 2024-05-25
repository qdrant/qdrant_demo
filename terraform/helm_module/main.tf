resource "helm_release" "qdrant_demo" {
  name      = "qdrant-demo"
  chart     = "../charts/qdrant_demo"
  namespace = "qdrant-services"
  depends_on = [helm_release.qdrant, kubernetes_namespace.qdrant-services]
}

resource "helm_release" "qdrant" {
  name      = "qdrant"
  chart     = "../charts/qdrant"
  namespace = "qdrant-services"
  depends_on = [kubernetes_namespace.qdrant-services]
  set {
    name  = "replicaCount"
    value = var.replicaCount
  }
}