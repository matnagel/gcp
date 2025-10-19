resource "google_project_service" "cloudbuild" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"
}

resource "google_storage_bucket" "deployment_bucket" {
  project       = var.project_id
  name          = "${var.project_id}-deployment"
  location      = var.region
  force_destroy = true
}

resource "google_cloudbuild_trigger" "default" {
  project  = var.project_id
  name     = "${var.github_repo}-trigger"
  location = var.region

  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = var.github_branch
    }
  }

  filename = "cloudbuild.yaml"
}
