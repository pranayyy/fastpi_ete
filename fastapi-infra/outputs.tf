output "ecs_public_ip" {
  description = "App Public IP (Fargate Task)"
  value       = aws_ecs_service.fastapi_service.network_configuration[0].assign_public_ip
}
