resource "google_storage_bucket" "bucket" {
  name          = "${var.bucket_config.name}-${var.basic_config.environment}"
  force_destroy = var.bucket_config.force_destroy
  location      = var.basic_config.gcp_region
  project       = var.basic_config.gcp_project_id
}
