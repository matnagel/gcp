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

resource "google_cloudfunctions_function" "billing-nuke" {
  name        = "billing-nuke"
  description = "Controls budget"
  runtime     = "python38"


  max_instances = 1
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.deployment-bucket.name
  source_archive_object = google_storage_bucket_object.billing-nuke-archive.name
  timeout               = 60
  entry_point           = "check_billing"

  ingress_settings = "ALLOW_INTERNAL_ONLY"

  event_trigger {
      event_type= "google.pubsub.topic.publish"
      resource= "projects/${var.project}/topics/${google_pubsub_topic.budget-topic.name}"
  }

  environment_variables = {
    PROJECT_ID = var.project
  }
}
