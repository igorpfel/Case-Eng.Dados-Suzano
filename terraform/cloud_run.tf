
# resource "google_cloud_run_service" "etl_service" {
#   name     = "etl-pipeline"
#   location = var.region
#   project  = var.project_id
#
#   template {
#     spec {
#       containers {
#         image = var.container_image
#       }
#     }
#   }
#
#   traffic {
#     percent         = 100
#     latest_revision = true
#   }
# }
