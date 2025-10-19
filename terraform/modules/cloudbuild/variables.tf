variable "project" {
  description = "The ID of the GCP project."
  type        = string
}

variable "region" {
  description = "The region for the Cloud Build trigger."
  type        = string
}

variable "github-owner" {
  description = "The owner of the GitHub repository."
  type        = string
}

variable "github-repo" {
  description = "The name of the GitHub repository."
  type        = string
}

variable "github-branch" {
  description = "The branch of the GitHub repository to trigger builds from."
  type        = string
  default     = "main"
}

variable "service_account" {
  description = "The service account to use for the Cloud Build trigger."
  type        = string
}