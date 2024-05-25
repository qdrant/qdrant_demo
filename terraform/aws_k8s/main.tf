data "aws_availability_zones" "available" {}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.1"

  name            = "${var.name}-vpc"
  cidr            = "172.16.0.0/16"
  azs             = data.aws_availability_zones.available.names
  private_subnets = ["172.16.1.0/24", "172.16.2.0/24", "172.16.3.0/24"]
  public_subnets  = ["172.16.4.0/24", "172.16.5.0/24", "172.16.6.0/24"]

  enable_nat_gateway      = true
  single_nat_gateway      = true
  map_public_ip_on_launch = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.name
  cluster_version = "1.29"
  subnet_ids      = module.vpc.private_subnets

  vpc_id                          = module.vpc.vpc_id
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  eks_managed_node_groups = {
    first = {
      desired_size = var.desired_capacity
      max_size     = var.max_capacity
      min_size     = var.min_capacity

      instance_types               = ["m5n.large"]
      capacity_type                = "SPOT"
      iam_role_additional_policies = { AmazonEBSCSIDriverPolicy = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy" }
    }
  }

  enable_cluster_creator_admin_permissions = true

  cluster_addons = {
    coredns            = {}
    kube-proxy         = {}
    vpc-cni            = {}
    aws-ebs-csi-driver = {}

  }


  access_entries = {
    # Provide access to the EKS cluster to the user ( Web User )
    user_access = {
      kubernetes_groups = []
      principal_arn     = var.user_arn

      policy_associations = {
        example = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
          access_scope = {
            type = "cluster"
          }
        }
      }
    }
  }


  # IMPORTANT
  node_security_group_additional_rules = merge(
    local.ingress_rules,
    local.egress_rules
  )
}

# Port needed to solve the error
# Internal error occurred: failed calling 
# webhook "namespace.sidecar-injector.istio.io": failed to 
# call webhook: Post "https://istiod.istio-system.svc:443/inject?timeout=10s": # context deadline exceeded
resource "aws_security_group_rule" "allow_sidecar_injection" {
  description = "Webhook container port, From Control Plane"
  protocol    = "tcp"
  type        = "ingress"
  from_port   = 15017
  to_port     = 15017

  security_group_id        = module.eks.node_security_group_id
  source_security_group_id = module.eks.cluster_primary_security_group_id
}