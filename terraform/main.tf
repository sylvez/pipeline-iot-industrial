terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

# Esto le dice a Terraform que queremos una imagen de Postgres
resource "docker_image" "postgres" {
  name         = "postgres:15-alpine"
  keep_locally = false
}

# Esto le dice a Terraform que cree el contenedor
resource "docker_container" "postgres_db" {
  image = docker_image.postgres.image_id
  name  = "iot_db_terraform"
  
  # ESTO ES LO QUE FALTABA: Las credenciales
  env = [
    "POSTGRES_USER=admin",
    "POSTGRES_PASSWORD=supersecreto",
    "POSTGRES_DB=sensores_terraform"
  ]

  ports {
    internal = 5432
    external = 5433 
  }
}