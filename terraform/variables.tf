# Set these two variables in a sibling terraform.tfvars file
variable "credentials_file" {}
variable "project" {}

variable "environment" {
  type    = string
  default = "development"
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
