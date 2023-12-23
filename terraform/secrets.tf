module "coinbase_api_key_secret" {
  source      = "./modules/secret"
  environment = var.environment
  secret_id   = "coinbase_api_key"
  secret_data = var.coinbase_api_key
}

module "coinbase_secret_key_secret" {
  source      = "./modules/secret"
  environment = var.environment
  secret_id   = "coinbase_secret_key"
  secret_data = var.coinbase_secret_key
}

module "telegram_bot_token_secret" {
  source      = "./modules/secret"
  environment = var.environment
  secret_id   = "telegram_bot_token"
  secret_data = var.telegram_bot_token
}

module "telegram_chat_id_secret" {
  source      = "./modules/secret"
  environment = var.environment
  secret_id   = "telegram_chat_id"
  secret_data = var.telegram_chat_id
}
