resource "google_storage_bucket" "deployment_bucket" {
  project       = var.project
  name          = "${var.project}-deployment"
  location      = var.region
  force_destroy = true
}

resource "google_cloudbuild_trigger" "default" {
  project  = var.project
  name     = "${var.github-repo}-trigger"
  location = var.region

  github {
    owner = var.github-owner
    name  = var.github-repo
    push {
      branch = "^${var.github-branch}$"
    }
  }

  filename = "cloudbuild.yaml"
}
