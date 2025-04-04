module "enable_google_apis" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "18.0.0"

  project_id = var.project_id

  activate_apis = [
    "artifactregistry.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudresourcemanager.googleapis.com", # This is required for the Project Factory to look up the GCP organization
    "cloudscheduler.googleapis.com",
    "pubsub.googleapis.com",
    "secretmanager.googleapis.com",
    # Required for Cloud Run Functions
    "eventarc.googleapis.com",
    "run.googleapis.com"
  ]

  disable_dependent_services  = false
  disable_services_on_destroy = false
}
