
variable "project_id" {
  description = "The ID of the GCP project."
  type        = string
}

variable "region" {
  description = "The region for the Cloud Build trigger."
  type        = string
}

variable "github_owner" {
  description = "The owner of the GitHub repository."
  type        = string
}

variable "github_repo" {
  description = "The name of the GitHub repository."
  type        = string
}

variable "github_branch" {
  description = "The branch of the GitHub repository to trigger builds from."
  type        = string
  default     = "main"
}
