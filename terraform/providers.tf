locals {
  region = "us-central1"
  zone   = "us-central1-c"
}

# Create a Google Cloud project that depends on the activation of the APIs so
# that the APIs are enabled before the project resources are created. This
# requires diligent usage of data.google_project.project.project_id instead of
# var.project_id in the resources that depend on the project.
data "google_project" "project" {
  project_id = var.project_id
  depends_on = [module.enable_google_apis]
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.17.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 6.17.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = local.region
  zone    = local.zone
}

provider "google-beta" {
  project = var.project_id
  region  = local.region
  zone    = local.zone
}
