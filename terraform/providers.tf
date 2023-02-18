locals {
  region = "us-central1"
  zone   = "us-central1-c"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.75.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "3.90.1"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = local.region
  zone    = local.zone
}

provider "google-beta" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = local.region
  zone    = local.zone
}
