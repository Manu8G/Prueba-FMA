# Bloque especial para definir estructura de terraform
terraform {
  backend "s3" {
    bucket = "tf-FMA"
    key = "servidor/terraform.tfstate"
    region = "eu-west-1"    # Probar si funciona con local.region
    dynamodb_table = "tf-FMA-locks"
    encrypt = true
  }
}

# Definimos el provider como AWS
provider "aws" {
  region = local.region
  shared_config_files = [ "/home/manuel/.aws/config" ]
  shared_credentials_files = [ "/home/manuel/.aws/credentials" ]
}


resource "aws_s3_bucket" "terraform_state" {
  bucket = "tf-FMA"
  
  lifecycle {
    prevent_destroy = true      # Este elemento no se destruira al hacer destroy
  }

  versioning {
    enabled = true              # Habra gestor de versiones
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"      # Encriptacion de los datos en disco
      }
    }
  }
}


# Creacion de la tabla que nos permitira tener los locks, con ello evitaremos condiciones de carrera
resource "aws_dynamodb_table" "terraform_locks" {
  name = "tf-FMA-locks"
  billing_mode = "PAY_PER_REQUEST"  # Entraria en el free tier
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}


locals{
  region = "eu-west-1"
  ami = var.ubuntu_ami[local.region]
}


# Definimos un "data source" el cual nos permite obtener informacion de AWS, en este caso de una aviability zone la cual usaremos mas abajo
data "aws_subnet" "public_subnet"{
  for_each = var.servidores
  availability_zone = "${local.region}${each.value.az}"
}


# Creamos las instancias de EC2 con AMI(Amazon Machine Image) Ubuntu 22 y con instance_type (tamaño de la imagen)
resource "aws_instance" "Servidor" {
  for_each = var.servidores
  ami = local.ami
  instance_type = var.tipo_instancia
  subnet_id = data.aws_subnet.public_subnet[each.key].id    # Gracias al "Data Source" definido anteriormente podemos obtener la ip de la AZ
  # El each.key seria "ser-1" y ser-2
  vpc_security_group_ids = [aws_security_group.mi_grupo_de_seguridad.id]

  # Script de inicio aqui hay que poner el docker
  user_data = <<-EOF
              #!/bin/bash
              echo "Hola terraform! Aqui ${each.value.nombre}" > index.html
              nohup busybox httpd -f -p ${var.puerto_servidor} &
              EOF

  tags = {
    Name = each.value.nombre # Nombre del servidor
  }
}


# Creacion del grupo de seguridad para limitar el acceso
resource "aws_security_group" "mi_grupo_de_seguridad" {
  name = "primer-servidor-sg"
  vpc_id = data.aws_vpc.default.id  

  ingress {
    # cidr_blocks = ["0.0.0.0/0"]    -> con esta linea cualquiera podria acceder al lb (load balancer)
    # Con la siguiente linea que sustituye a la anterior, solo los miembros del security group podrian acceder al lb
    # Esto permite que solo la carga mandada desde el load balancer pueda acceder a los servidores
    security_groups = [aws_security_group.alb.id]
    description = "Acceso al puerto 8080 desde el exterior"
    from_port = var.puerto_servidor
    to_port = var.puerto_servidor
    protocol = "TCP"
  }
}


# Definimos el application load balancer
resource "aws_lb" "alb" {
  load_balancer_type = "application"
  name = "terraformers-alb"
  security_groups = [aws_security_group.alb.id]
  subnets = [for subnet in data.aws_subnet.public_subnet : subnet.id]      # Donde va a repartir la carga
}


# Definimos el security group del load balancer
resource "aws_security_group" "alb" {
  name = "alb-sg"
  vpc_id = data.aws_vpc.default.id  # Virtual private cloud

  # Trafico entrante permitido, permite que se le llame desde el listener
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    description = "Acceso al puerto 80 desde el exterior"
    from_port = var.puerto_lb
    to_port = var.puerto_lb
    protocol = "TCP"
  }
  
  # Trafico saliente permitido, permite llamar a las instancias de los servidores
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    description = "Acceso al puerto 8080 de nuestros servidores"
    from_port = var.puerto_servidor
    to_port = var.puerto_servidor
    protocol = "TCP"
  }
}


data "aws_vpc" "default" {  # Devuelve la VPC que tenemos por defecto en aws (solo si default vale true)
  default = true
}


# Crea "grupos" de servidores para enfocar la carga que va llegando
resource "aws_lb_target_group" "this" { 
  name = "terraformers-alb-target-group"
  port = var.puerto_lb
  vpc_id = data.aws_vpc.default.id # virtual private cloud
  protocol = "HTTP"

   # Si devuelve un 200 significa que esta funcionando correctamente y por tanto el valanceador de carga le puede mandar peticiones, si no lo esta no le manda carga
   health_check { 
     enabled = true
     matcher = "200"
     path = "/"
     port = var.puerto_servidor
     protocol = "HTTP"
   }
}


# Añadimos los servidores al grupo de attachement
resource "aws_lb_target_group_attachment" "Servidor" {
 for_each = var.servidores
 target_group_arn = aws_lb_target_group.this.arn # Indicador del target group
 target_id = aws_instance.Servidor[each.key].id # Indicador del servidor que se añade al group attachement
 port = var.puerto_servidor
}


# Vamos a crear el escuchador que recibira las peticiones y le pasara estas al balanceador de carga para que las mande a los respectivos servidores
resource "aws_lb_listener" "this" {
  load_balancer_arn = aws_lb.alb.id
  port = var.puerto_lb

  default_action {
    target_group_arn = aws_lb_target_group.this.arn
    type = "forward"
  }
}

