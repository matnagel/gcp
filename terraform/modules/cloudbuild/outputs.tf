
output "trigger_id" {
  description = "The ID of the Cloud Build trigger."
  value       = google_cloudbuild_trigger.default.id
}

output "deployment_bucket_name" {
  description = "The name of the GCS bucket for deployments."
  value       = google_storage_bucket.deployment_bucket.name
}
