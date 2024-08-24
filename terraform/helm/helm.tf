resource "helm_release" "backend" {
  name       = "digbackend"
  namespace  = "dig"
  repository = "file://charts/backend-chart"
  chart      = "backend-chart"
  version    = "0.0.1"

  values = [
    templatefile("helm-values/backend.yaml", {})
  ]
}

resource "helm_release" "frontend" {
  name       = "digfrontend"
  namespace  = "dig"
  repository = "file://charts/frontend-chart"
  chart      = "frontend-chart"
  version    = "0.0.2"

  values = [
    templatefile("helm-values/frontend.yaml", {})
  ]
}

resource "helm_release" "postgres" {
  name       = "postgresql"
  namespace  = "dig"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"
  version    = "15.5.23"

  values = [
    templatefile("helm-values/postgres.yaml", {})
  ]
}