variable "name"{ 
    description = "The name of the EKS cluster"
    type = string
    default = "qdrant-demo"
}
variable "user_arn" {
    description = "The ARN of the user to grant access to the EKS cluster"
    type = string
    default = ""
}
variable "desired_capacity" {
    description = "The desired capacity of the autoscaling group"
    type        = number
    default     = 2
}
variable "max_capacity" {
    description = "The max capacity of the autoscaling group"
    type        = number
    default     = 4
}
variable "min_capacity" {
    description = "The min capacity of the autoscaling group"
    type        = number
    default     = 2
}