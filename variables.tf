# En este archivo voy a definir las varibales que usaremos en nuestro codigo terraform lo cual nos permitira realizar camibar de forma mucho mas rapida
variable "puerto_servidor" {
  description = "Puerto para las instancias EC2"
  type = number
  default = 8080

  validation {
    condition = var.puerto_servidor > 0 && var.puerto_servidor <= 65536
    error_message = "El valor del puerto debe estar entre 1 y 65536"
  }

}


variable "puerto_lb" {
  description = "Puerto del load balancer"
  type = number
  default = 80
}


variable "tipo_instancia" {
  description = "Tipo de instancia de la EC2"
  type = string
  default = "t2.micro"
}


variable "ubuntu_ami" {
   description = "AMI de la region"
   type = map(string)

    default = {
        eu-west-1 = "ami-0a422d70f727fe93e"
        us-west-2 = "ami-9851g6efsg21156r5"
    }

}

variable "servidores" {
  description = "Mapa de los servidores"
  type = map(object({
    nombre = string,
    az = string
    })
  )
  default = {
    "ser-1" = { nombre = "Servidor_1", az = "a"},
    "ser-2" = { nombre = "Servidor_2", az = "b"}
  }
}