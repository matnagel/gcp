terraform {
  backend "gcs" {}
  google = {
    source  = "hashicorp/google"
    version = "7.7.0"
  }
}
