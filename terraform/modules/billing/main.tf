locals {
  deploy_zip = "../../python/billing/billing_nuke.zip"
}

resource "google_pubsub_topic" "budget_topic" {
  name = "budget-verification"
}

resource "random_string" "zip_id" {
  length  = 10
  special = false
  upper   = false
  keepers = {
    sha256 = filesha256(local.deploy_zip)
  }
}

resource "google_storage_bucket_object" "billing_nuke_archive" {
  name   = "billing/${random_string.zip_id.result}_billing_nuke.zip"
  bucket = google_storage_bucket.deployment_bucket.name
  source = local.deploy_zip
}

resource "google_storage_bucket" "deployment_bucket" {
  name                        = "${var.project}-deployment"
  location                    = var.region
  uniform_bucket_level_access = true
}

resource "google_service_account" "check_billing" {
  account_id  = "check-billing"
  description = "Budget supervision"
}

resource "google_billing_account_iam_member" "admin_binding" {
  billing_account_id = var.billing-account
  role               = "roles/billing.admin"
  member             = "serviceAccount:${google_service_account.check_billing.email}"
}

resource "google_cloudfunctions2_function" "billing_nuke" {
  name        = "billing-nuke"
  location    = var.region
  description = "Controls budget"

  build_config {
    runtime     = "python312"
    entry_point = "check_billing"
    source {
      storage_source {
        bucket = google_storage_bucket.deployment_bucket.name
        object = google_storage_bucket_object.billing_nuke_archive.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    available_memory      = "128Mi"
    timeout_seconds       = 60
    ingress_settings      = "ALLOW_INTERNAL_ONLY"
    service_account_email = google_service_account.check_billing.email
    environment_variables = {
      PROJECT_ID = var.project
      BILLING_ID = var.billing-account
    }
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.budget_topic.id
    retry_policy   = "RETRY_POLICY_DO_NOT_RETRY"
  }
}

moved {
  from = google_pubsub_topic.budget-topic
  to   = google_pubsub_topic.budget_topic
}

moved {
  from = google_storage_bucket_object.billing-nuke-archive
  to   = google_storage_bucket_object.billing_nuke_archive
}

moved {
  from = google_storage_bucket.deployment-bucket
  to   = google_storage_bucket.deployment_bucket
}

moved {
  from = google_service_account.check-billing
  to   = google_service_account.check_billing
}

moved {
  from = google_billing_account_iam_member.admin-binding
  to   = google_billing_account_iam_member.admin_binding
}

moved {
  from = google_cloudfunctions2_function.billing-nuke
  to   = google_cloudfunctions2_function.billing_nuke
}