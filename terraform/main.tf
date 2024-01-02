locals {
  deposit_function_name     = "${var.environment}-coinbase-deposit"
  deposit_pubsub_topic_name = "${var.environment}-coinbase-deposit-requests"
  orders_function_name      = "${var.environment}-coinbase-orders"
  orders_pubsub_topic_name  = "${var.environment}-coinbase-orders-requests"
}

# Orders

module "orders_function" {
  source               = "./modules/function"
  project_id           = var.project_id
  function_name        = local.orders_function_name
  pubsub_topic_name    = local.orders_pubsub_topic_name
  function_entry_point = "coinbase_orders"
  environment          = var.environment
}

resource "google_pubsub_topic" "orders_requests" {
  name = local.orders_pubsub_topic_name
}

resource "google_cloud_scheduler_job" "orders_job_1st" {
  name        = "${var.environment}-coinbase-orders-job-1st"
  description = "Job that executes orders on the 1st of every month"
  schedule    = "0 0 1 * *"
  time_zone   = var.time_zone

  pubsub_target {
    topic_name = google_pubsub_topic.orders_requests.id
    data       = base64encode(jsonencode(var.purchase_orders))
  }
}

resource "google_cloud_scheduler_job" "orders_job_15th" {
  name        = "${var.environment}-coinbase-orders-job-15th"
  description = "Job that executes orders on the 15th of every month"
  schedule    = "0 0 15 * *"
  time_zone   = var.time_zone

  pubsub_target {
    topic_name = google_pubsub_topic.orders_requests.id
    data       = base64encode(jsonencode(var.purchase_orders))
  }
}

# Deposit

module "deposit_function" {
  source               = "./modules/function"
  project_id           = var.project_id
  function_name        = local.deposit_function_name
  pubsub_topic_name    = local.deposit_pubsub_topic_name
  function_entry_point = "coinbase_deposit"
  environment          = var.environment
}

resource "google_pubsub_topic" "deposit_requests" {
  name = local.deposit_pubsub_topic_name
}

resource "google_cloud_scheduler_job" "deposit_job_1st" {
  name        = "${var.environment}-coinbase-deposit-job-1st"
  description = "Job that executes a deposit on the 1st of every month"
  schedule    = "0 0 1 * *"
  time_zone   = var.time_zone

  pubsub_target {
    topic_name = google_pubsub_topic.deposit_requests.id
    data       = base64encode(jsonencode(var.deposit_request))
  }
}

resource "google_cloud_scheduler_job" "deposit_job_15th" {
  name        = "${var.environment}-coinbase-deposit-job-15th"
  description = "Job that executes a deposit on the 15th of every month"
  schedule    = "0 0 15 * *"
  time_zone   = var.time_zone

  pubsub_target {
    topic_name = google_pubsub_topic.deposit_requests.id
    data       = base64encode(jsonencode(var.deposit_request))
  }
}
