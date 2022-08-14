resource "google_storage_bucket" "build-logs-bucket" {
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

resource "google_storage_bucket" "tf-state" {
  name                        = "${var.project}-tf-state"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}
