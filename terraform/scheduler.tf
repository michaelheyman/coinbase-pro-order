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
