resource "google_storage_bucket" "build-logs-bucket" {
  name                        = "${var.project}-build-logs"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "website-resources" {
  name                        = "${var.project}-website-resources"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "website-deployment" {
  name                        = "${var.project}-deployment"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "website-configuration" {
  name                        = "${var.project}-website-configuration"
  project                     = var.project
  location                    = var.region
  labels                      = {}
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "website-tf-state" {
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
