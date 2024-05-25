resource "helm_release" "istio-base" {
  name             = "istio-base"
  namespace        = "istio-system"
  chart            = "../charts/istio/base"
  wait             = true
  create_namespace = true
  set {
    name  = "defaultRevision"
    value = "default"
  }
}

resource "helm_release" "istiod" {
  name             = "istiod"
  namespace        = "istio-system"
  chart            = "../charts/istio/istiod"
  wait             = true
  create_namespace = true
  depends_on       = [helm_release.istio-base]
  set {
    name  = "meshConfig.accessLogFile"
    value = "/dev/stdout"
  }

}

resource "helm_release" "istio-ingress" {
  name             = "istio-ingress"
  namespace        = "istio-ingress"
  chart            = "../charts/istio/gateway"
  depends_on       = [helm_release.istiod, kubernetes_namespace.istio-ingress]
}