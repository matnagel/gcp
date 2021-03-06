resource "google_project_service" "iam_api" {
  project = var.project
  service = "iam.googleapis.com"
}

resource "google_project_service" "resource_api" {
  project = var.project
  service = "cloudresourcemanager.googleapis.com"
}

resource "google_project_service" "scheduler_api" {
  project = var.project
  service = "cloudscheduler.googleapis.com"
}

resource "google_project_service" "functions_api" {
  project = var.project
  service = "cloudfunctions.googleapis.com"
}

resource "google_project_service" "billing_api" {
  project = var.project
  service = "cloudbilling.googleapis.com"
}
