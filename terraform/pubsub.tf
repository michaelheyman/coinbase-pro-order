locals {
  deposit_pubsub_topic_name = "${var.environment}-coinbase-deposit-requests"
  orders_pubsub_topic_name  = "${var.environment}-coinbase-orders-requests"
}

resource "google_pubsub_topic" "orders_requests" {
  name = local.orders_pubsub_topic_name
}

resource "google_pubsub_topic" "deposit_requests" {
  name = local.deposit_pubsub_topic_name
}
