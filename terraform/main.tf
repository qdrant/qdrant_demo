module "aws_k8s" {
  source           = "./aws_k8s"
  name             = var.name
  desired_capacity = 3
  max_capacity     = 6
  min_capacity     = 3
  user_arn         = var.user_arn
}
/*
module "helm_module" {
  source     = "./helm_module"
  replicaCount = 3
  depends_on = [module.aws_k8s]
}*/
/*
module "cognito" {
  source     = "./aws_cognito"
  name       = var.name
  depends_on = [module.aws_k8s]
}
*/