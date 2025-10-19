resource "google_project_service" "cloudbuild" {
  project = var.project
  service = "cloudbuild.googleapis.com"
}

module "cloudbuild" {
  source       = "../cloudbuild"
  project      = var.project
  region       = var.region
  github-owner = var.github-owner
  github-repo  = var.github-repo
}
