provider "google" {
  project = var.project
  zone = var.zone
}

module "api_setup" {
  source      = "../modules/api_setup"
  project  = var.project
}	

module "billing" {
  source      = "../modules/billing"
  project  = var.project
  region = var.region
  billing-account = var.billing-account
}
