resource "google_storage_bucket" "build-logs-bucket" {
  name     = "${var.project}-build-logs"
  project = var.project
  location = var.region
  uniform_bucket_level_access = true
}
