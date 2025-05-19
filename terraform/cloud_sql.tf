
resource "google_sql_database_instance" "investing_instance" {
  name             = "investing-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled    = true
      authorized_networks {
        name  = "liberar-tudo"
        value = "0.0.0.0/0"
      }
    }
  }
}

resource "google_sql_user" "default" {
  name     = "postgres"
  instance = google_sql_database_instance.investing_instance.name
  password = "1234"
}

resource "google_sql_database" "investing" {
  name     = "investing"
  instance = google_sql_database_instance.investing_instance.name
}
