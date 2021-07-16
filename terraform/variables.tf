variable "credentials_file" {
  type    = string
  default = "<PATH_TO_CREDENTIALS_FILE>"
}

variable "project" {
  type    = string
  default = "<PROJECT_ID>"
}

variable "time_zone" {
  type    = string
  default = "America/Los_Angeles"
}

variable "purchase_orders" {
  type = list(map(string))
  default = [
    {
      "product_id" = "ETH-USD",
      "price"      = "25.0"
    }
  ]
}

variable "function_name" {
  type    = string
  default = "coinbase_orders"
}

variable "pubsub_topic_name" {
  type    = string
  default = "purchase-requests"
}
