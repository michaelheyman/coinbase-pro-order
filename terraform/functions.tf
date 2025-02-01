locals {
  deposit_function_name = "${var.environment}-coinbase-deposit"
  orders_function_name  = "${var.environment}-coinbase-orders"
}

module "orders_function" {
  source                = "./modules/function"
  project_id            = var.project_id
  function_name         = local.orders_function_name
  function_description  = "Cloud Function that executes orders on Coinbase"
  pubsub_topic_name     = local.orders_pubsub_topic_name
  function_entry_point  = "coinbase_orders"
  environment           = var.environment
  region                = var.region
  service_account_email = google_service_account.orders_cf_service_account.email
}

module "deposit_function" {
  source                = "./modules/function"
  project_id            = var.project_id
  function_name         = local.deposit_function_name
  function_description  = "Cloud Function that deposits funds into Coinbase"
  pubsub_topic_name     = local.deposit_pubsub_topic_name
  function_entry_point  = "coinbase_deposit"
  environment           = var.environment
  service_account_email = google_service_account.deposit_cf_service_account.email
}
