resource "google_project_service" "cloudbuild" {
  project = var.project
  service = "cloudbuild.googleapis.com"
}

resource "google_service_account" "git_build" {
  project      = var.project
  account_id   = "git-build"
  display_name = "Git Build"
}

module "cloudbuild" {
  source          = "../cloudbuild"
  project         = var.project
  region          = var.region
  github-owner    = var.github-owner
  github-repo     = var.github-repo
  service_account = google_service_account.git_build.id
}