output "dns_publica_server" {
  description = "DNS publica del servidor"
  value = [for Servidor in aws_instance.Servidor :
  "http://${Servidor.public_dns}:${var.puerto_servidor}"
  ]
}

output "IPV4_server" {
  description = "IPV4 publica del servidor"
  value = [for Servidor in aws_instance.Servidor :
  "http://${Servidor.public_ip}:${var.puerto_servidor}"
  ]
}

output "dns_publica_load_balancer" {
  description = "DNS publica del load balancer"
  value = "http://${aws_lb.alb.dns_name}"
}


