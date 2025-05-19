resource "google_composer_environment" "etl_airflow" {
  name    = "composer-etl"
  region  = var.region
  project = var.project_id

  config {
    software_config {
      image_version = "composer-3-airflow-2.10.5"
      env_variables = {}
    }
  }
}