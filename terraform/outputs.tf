output "aws_k8s_cluster_name" {
  value = "export KUBERNETES_MASTER=${module.aws_k8s.cluster_name}"
}
/*
output "token_signing_key" {
  value = "https://cognito-idp.${var.aws_region}.amazonaws.com/${module.cognito.id}/.well-known/jwks.json"
}
output "cognito_login_url" {
  value = "https://${module.cognito.domain}.auth.${var.aws_region}.amazoncognito.com/login?response_type=token&client_id=${module.cognito.user_pool_client_id}&response_type=token&scope=email+openid+profile&redirect_uri=${module.cognito.callback_urls[0]}"
}*/