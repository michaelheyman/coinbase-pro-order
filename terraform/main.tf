module "function" {
  source               = "./modules/function"
  project              = var.project
  function_name        = var.function_name
  pubsub_topic_name    = var.pubsub_topic_name
  function_entry_point = "coinbase_orders"
}

resource "google_pubsub_topic" "purchase_requests" {
  name = var.pubsub_topic_name
}

resource "google_cloud_scheduler_job" "first_job" {
  name        = "coinbase-first-job"
  description = "Job that runs on the 1st of every month"
  schedule    = "0 0 1 * *"
  time_zone   = var.time_zone

  pubsub_target {
    topic_name = google_pubsub_topic.purchase_requests.id
    data       = base64encode(jsonencode(var.purchase_orders))
  }
}

resource "google_cloud_scheduler_job" "second_job" {
  name        = "coinbase-second-job"
  description = "Job that runs on the 15th of every month"
  schedule    = "0 0 15 * *"
  time_zone   = var.time_zone

  pubsub_target {
    topic_name = google_pubsub_topic.purchase_requests.id
    data       = base64encode(jsonencode(var.purchase_orders))
  }
}
