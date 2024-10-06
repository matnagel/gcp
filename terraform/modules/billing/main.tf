locals {
	deploy_zip = "/workspace/python/billing/billing_nuke.zip"
}

resource "google_pubsub_topic" "budget-topic" {
  name = "budget-verification"
}

resource "random_string" "zip_id" {
  length = 10
  special = false
  upper = false
  keepers = {
    sha256 = filesha256(local.deploy_zip)
  }
}

resource "google_storage_bucket_object" "billing-nuke-archive" {
  name   = "billing/${random_string.zip_id.result}_billing_nuke.zip"
  bucket = google_storage_bucket.deployment-bucket.name
  source = local.deploy_zip 
}

resource "google_storage_bucket" "deployment-bucket" {
  name     = "${var.project}-deployment"
  location = var.region
  uniform_bucket_level_access = true
}

resource "google_service_account" "check-billing" {
  account_id   = "check-billing"
  description = "Budget supervision"
}

resource "google_billing_account_iam_member" "admin-binding" {
  billing_account_id = var.billing-account
  role               = "roles/billing.admin"
  member             = "serviceAccount:${google_service_account.check-billing.email}"
}

resource "google_cloudfunctions_function" "billing-nuke" {
  name        = "billing-nuke"
  description = "Controls budget"
  runtime     = "python312"


  max_instances = 1
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.deployment-bucket.name
  source_archive_object = google_storage_bucket_object.billing-nuke-archive.name
  timeout               = 60
  entry_point           = "check_billing"

  ingress_settings = "ALLOW_INTERNAL_ONLY"

  service_account_email = google_service_account.check-billing.email

  event_trigger {
      event_type= "google.pubsub.topic.publish"
      resource= "projects/${var.project}/topics/${google_pubsub_topic.budget-topic.name}"
  }

  environment_variables = {
    PROJECT_ID = var.project
    BILLING_ID = var.billing-account
  }
}
