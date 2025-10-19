resource "google_project" "todo_project" {
  name            = "todo app hosting"
  project_id      = var.project
  billing_account = var.billing-account
}
