variable "name" {
  description = "The name of the EKS cluster"
  type        = string
  default     = "qdrant-demo"
}
variable "callback_urls" {
  description = "The callback URLs for the Cognito User Pool Client"
  type        = list(string)
  default     = ["http://localhost:8000/auth/callback"]
}

variable "logout_urls" {
  description = "The logout URLs for the Cognito User Pool Client"
  type        = list(string)
  default     = ["http://localhost:8000/auth/logout"]
}
