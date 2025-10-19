provider "google" {
  project = var.command-project
  zone    = var.zone
}

module "api_setup" {
  source  = "../modules/api_setup"
  project = var.command-project
}

module "billing" {
  source          = "../modules/billing"
  project         = var.command-project
  region          = var.region
  billing-account = var.billing-account
  depends_on      = [module.api_setup]
}

module "webpage" {
  source  = "../modules/webpage"
  project = var.webpage-project
  region  = var.region
}

module "stockrecords" {
  source  = "../modules/stockrecords"
  project = var.stockrecord-project
  region  = var.region
}

module "todo" {
  source          = "../modules/todo"
  project         = var.todo-project
  billing-account = var.billing-account
}
