variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}
variable "name" {
  description = "The name of the EKS cluster"
  type        = string
  default     = "qdrant-demo"
}
variable "user_arn" {
  description = "The ARN of the user to grant access to the EKS cluster"
  type        = string
  default     = ""
}