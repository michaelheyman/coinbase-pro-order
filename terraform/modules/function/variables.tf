variable "project_id" {
  description = "The ID of the project in which resources will be managed."
}

variable "function_name" {
  description = "The name of the Cloud Function to be created."
}

variable "function_description" {
  description = "The description of the Cloud Function to be created."
}

variable "function_entry_point" {
  description = "The name of a method in the function source which will be called when the function is executed."
}

variable "pubsub_topic_name" {
  description = "The name of the Pub/Sub topic to be created."
}

variable "environment" {
  description = "The environment for which resources will be managed. This variable is typically used to differentiate between development, staging, and production environments."
}

variable "region" {
  description = "The region in which resources will be managed."
  default     = "us-central1"
}

variable "service_account_email" {
  description = "The email of the service account to run the cloud function"
  type        = string
  default     = null # This means GCP will create a default service account
}
