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
  name                        = "${var.project_id}-${var.function_name}-function" #tfsec:ignore:google-storage-enable-ubla
  location                    = var.region
  uniform_bucket_level_access = true
}

# Add source code zip to bucket
resource "google_storage_bucket_object" "zip" {
  # Append file MD5 to force bucket to be recreated
  name   = "${var.function_name}-${data.archive_file.source.output_md5}/function-source.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.source.output_path
}


# Create Cloud Function
resource "google_cloudfunctions2_function" "function" {
  name        = var.function_name
  location    = var.region
  description = var.function_description

  build_config {
    runtime     = "python312"
    entry_point = var.function_entry_point
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.zip.name
      }
    }
  }

  service_config {
    environment_variables = {
      ENVIRONMENT       = var.environment
      GOOGLE_PROJECT_ID = var.project_id
    }
    ingress_settings      = "ALLOW_INTERNAL_ONLY"
    service_account_email = var.service_account_email
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = "projects/${var.project_id}/topics/${var.pubsub_topic_name}" # TODO: pass topic id here instead
    retry_policy   = "RETRY_POLICY_DO_NOT_RETRY"
  }
}
