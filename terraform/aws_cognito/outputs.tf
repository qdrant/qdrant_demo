output "id" {
  value = aws_cognito_user_pool.user_pool.id
}
output "user_pool_client_id" {
  value = aws_cognito_user_pool_client.user_pool_client.id
}
output "domain" {
  value = aws_cognito_user_pool_domain.main.domain
}
output "callback_urls" {
  value = var.callback_urls
}
