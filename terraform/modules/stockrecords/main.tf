resource "google_storage_bucket" "build_logs_bucket" {
  name                        = "${var.project}-build-logs"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "configuration" {
  name                        = "${var.project}-configuration"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "tf_state" {
  name                        = "${var.project}-tf-state"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

moved {
  from = google_storage_bucket.build-logs-bucket
  to   = google_storage_bucket.build_logs_bucket
}

moved {
  from = google_storage_bucket.tf-state
  to   = google_storage_bucket.tf_state
}