
output "cloud_sql_connection_name" {
  value = google_sql_database_instance.investing_instance.connection_name
}

output "composer_airflow_uri" {
  value = google_composer_environment.etl_airflow.config[0].airflow_uri
}
