resource "aws_ssm_parameter" "vpc_id" {
  name  = "/${var.name}/vpc_id"
  type = "String"
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}
resource "aws_ssm_parameter" "eks_cluster_name" {
  name  = "/${var.name}/cluster_name"
  type = "String"
  description = "The name of the EKS cluster"
  value       = module.eks.cluster_name
}
