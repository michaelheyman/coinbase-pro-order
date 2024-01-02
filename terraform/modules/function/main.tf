locals {
  timestamp = formatdate("YYMMDDhhmmss", timestamp())
  root_dir  = abspath("../")
}

# Compress source code
data "archive_file" "source" {
  type       = "zip"
  source_dir = local.root_dir
  excludes = [
    ".idea",
    ".git",
    ".pytest_cache",
    ".vscode",
    "terraform",
    "tests",
  ]
  output_path = "/tmp/${var.function_name}-function-${local.timestamp}.zip"
}

# Create bucket that will host the source code
#tfsec:ignore:google-storage-enable-ubla
resource "google_storage_bucket" "bucket" {
  name = "${var.project_id}-${var.function_name}-function" #tfsec:ignore:google-storage-enable-ubla
  # uniform_bucket_level_access = true
  location = var.region
}

# Add source code zip to bucket
resource "google_storage_bucket_object" "zip" {
  # Append file MD5 to force bucket to be recreated
  name   = "${var.function_name}-${data.archive_file.source.output_md5}/function-source.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.source.output_path
}

# Enable Cloud Functions API
resource "google_project_service" "cf" {
  project = var.project_id
  service = "cloudfunctions.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Enable Cloud Build API
resource "google_project_service" "cb" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Create Cloud Function
resource "google_cloudfunctions_function" "function" {
  name    = var.function_name
  runtime = "python312"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/${var.pubsub_topic_name}"
  }
  entry_point = var.function_entry_point

  environment_variables = {
    ENVIRONMENT       = var.environment
    GOOGLE_PROJECT_ID = var.project_id
  }

  region = var.region
}
