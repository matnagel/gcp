resource "google_storage_bucket" "build_logs_bucket" {
  name                        = "${var.project}-build-logs"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "website_resources" {
  name                        = "${var.project}-website-resources"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "website_deployment" {
  name                        = "${var.project}-deployment"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "website_configuration" {
  name                        = "${var.project}-website-configuration"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "website_tf_state" {
  name                        = "${var.project}-tf-state"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_project_service" "appengine_api" {
  project = var.project
  service = "appengine.googleapis.com"
}

moved {
  from = google_storage_bucket.build-logs-bucket
  to   = google_storage_bucket.build_logs_bucket
}

moved {
  from = google_storage_bucket.website-resources
  to   = google_storage_bucket.website_resources
}

moved {
  from = google_storage_bucket.website-deployment
  to   = google_storage_bucket.website_deployment
}

moved {
  from = google_storage_bucket.website-configuration
  to   = google_storage_bucket.website_configuration
}

moved {
  from = google_storage_bucket.website-tf-state
  to   = google_storage_bucket.website_tf_state
}