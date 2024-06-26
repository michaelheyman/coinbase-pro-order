# Set these two variables in a sibling terraform.tfvars file
variable "credentials_file" {
  description = "Path to the credentials file. See README for details."
  type        = string
}

variable "deposit_request" {
  description = "Deposit request."
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
  description = "List of purchase order numbers to deploy to the environment."
  type = list(object({
    product_id = string # The product_id must match a valid product. The products list is available via the /products endpoint here: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproducts
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

variable "coinbase_api_key" {
  description = "Coinbase API key."
  type        = string
}

variable "coinbase_secret_key" {
  description = "Coinbase secret key."
  type        = string
}

variable "coinbase_trading_api_key" {
  description = "Coinbase Advanced Trading API key name."
  type        = string
}

variable "coinbase_trading_private_key" {
  description = "Coinbase Advanced Trading API private key."
  type        = string
}

variable "telegram_bot_token" {
  description = "Telegram bot token."
  type        = string
}

variable "telegram_chat_id" {
  description = "Telegram chat ID."
  type        = string
}
