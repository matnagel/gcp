provider "google" {
  project = var.command-project
  zone = var.zone
}

module "api_setup" {
  source      = "../modules/api_setup"
  project  = var.command-project
}	

module "billing" {
  source      = "../modules/billing"
  project  = var.command-project
  region = var.region
  billing-account = var.billing-account
}
