# Set these two variables in a sibling terraform.tfvars file
variable "deposit_request" {
  description = "Amount to be deposited to Coinbase by the deposit function."
  type = object({
    amount   = number
    currency = string
  })
}

variable "environment" {
  type    = string
  default = "development"
}

variable "time_zone" {
  type    = string
  default = "America/Los_Angeles"
}

variable "project_id" {
  description = "Project ID of the project to deploy to. See README for details."
  type        = string
}

variable "purchase_orders" {
  description = <<-EOT
    List of purchase order numbers to deploy to the environment. The minimum
    price for each purchase is 10.0 USD.

    To see the list of valid `product_id`s, run:

    curl https://api.exchange.coinbase.com/products | jq '.[].id' | sort -u
  EOT
  type = list(object({
    product_id = string
    price      = string
  }))

  validation {
    condition = alltrue([
      for order in var.purchase_orders : order.price >= 10.0
    ])
    error_message = "The minimum price for each purchase is 10.0 USD."
  }
}

variable "region" {
  description = "Region to deploy to."
  type        = string
  default     = "us-central1"
}

# Secrets

variable "coinbase_trading_api_key" {
  description = "Coinbase Advanced Trading API key name."
  type        = string
  sensitive   = true
}

variable "coinbase_trading_private_key" {
  description = "Coinbase Advanced Trading API private key."
  type        = string
  sensitive   = true
}

variable "telegram_bot_token" {
  description = "Telegram bot token."
  type        = string
  sensitive   = true
}

variable "telegram_chat_id" {
  description = "Telegram chat ID."
  type        = string
  sensitive   = true
}
