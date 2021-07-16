module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "11.1.0"

  project_id = var.project

  activate_apis = [
    "cloudfunctions.googleapis.com",
    "cloudresourcemanager.googleapis.com", # This is required for the Project Factory to look up the GCP organization
    "cloudscheduler.googleapis.com",
    "pubsub.googleapis.com"
  ]

  disable_dependent_services  = false
  disable_services_on_destroy = false
}
