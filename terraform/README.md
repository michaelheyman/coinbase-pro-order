# terraform

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Installing Terraform](#installing-terraform)
- [Installing `gcloud`](#installing-gcloud)
- [Set up Google Cloud Platform project](#set-up-google-cloud-platform-project)
- [Usage](#usage)
  - [Configuring Terraform](#configuring-terraform)
  - [Running Terraform](#running-terraform)
  - [Terraform Best-Practices](#terraform-best-practices)
    - [`tfsec`](#tfsec)
- [Troubleshooting](#troubleshooting)
  - [Disabled APIs](#disabled-apis)
- [Enhancements](#enhancements)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installing Terraform

Install Terraform by tapping into the Terraform keg and installing the CLI via `brew`:

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

For more up-to-date information, visit the [Terraform docs](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/gcp-get-started)
on this subject.

## Installing `gcloud`

Install the `gcloud` CLI by following the instructions
[here](https://cloud.google.com/sdk/docs/install), or by using `brew`:

```bash
brew install --cask google-cloud-sdk
```

Then, initialize the `gcloud` CLI:

```bash
gcloud init
```

And follow the instructions to authenticate.

## Set up Google Cloud Platform project

Follow these instructions to set up Google Cloud Platform project:

- [Create a GCP project](https://console.cloud.google.com/projectcreate)

For more up-to-date information, visit the [Terraform docs](https://learn.hashicorp.com/tutorials/terraform/google-cloud-platform-build)
on this subject.

## Usage

### Configuring Terraform

Create a `terraform.tfvars` file in this directory. Then, fill it with the
following variables with their appropriate values:

- `project_id`: this value is your GCP project id
- `deposit_request`: request that will be sent to Coinbase to deposit funds
- `purchase_orders`: although the config provides a default purchase, you're
encouraged to update this as well
- `coinbase_api_key`: this is the API key for your Coinbase account
- `coinbase_secret_key`: this is the secret key for your Coinbase account
- `coinbase_trading_api_key`: this is the trading API key for your Coinbase account
- `coinbase_trading_private_key`: this is the trading private key for your
Coinbase account
- `telegram_bot_token`: this is the token for your Telegram bot
- `telegram_chat_id`: this is the chat id for your Telegram bot`
- `environment`: set this to "production" to enable the trading

Example:

```terraform
project_id = "your-unique-gcp-project-id"
deposit_request = {
  amount   = 100.00
  currency = "USD"
}
purchase_orders = [
  {
    product_id = "BTC-USD"
    price      = 100.0
  }
]
coinbase_api_key             = "api-key"
coinbase_secret_key          = "secret-key"
coinbase_trading_api_key     = "trading-api-key"
coinbase_trading_private_key = "trading-private-key"
telegram_bot_token           = "bot-token"
telegram_chat_id             = "chat-id"
environment                  = "production"

```

Visit the [variable configuration file](./variables.tf) to view other values
that can be overridden.

### Running Terraform

Before running Terraform, you must initialize the directory:

```bash
terraform init
```

Then, you can optionally confirm that the configuration is valid:

```bash
terraform validate
```

Optionally, you can also view what infrastructure changes the Terraform
configuration will apply:

```bash
terraform plan
```

Any command that actually affects the infrastructure (`apply` or `destroy`) will
require you to authenticate with your Google Cloud account first:

```bash
gcloud auth application-default login
```

To apply the Terraform configuration run the following:

```bash
terraform apply
```

If you want to revert your changes simply destroy the created resources:

```bash
terraform destroy
```

### Terraform Best-Practices

#### `tfsec`

See [official docs](https://github.com/aquasecurity/tfsec#installation) for
installation instructions.

Usage:

```bash
tfsec . --tfvars-file variables.tf
```

## Troubleshooting

### Disabled APIs

The Terraform config attempts to enable the required APIs. It is worth
investing in making this process automated and robust as issues arise.

If that doesn't work follow the descriptive errors when attempting to plan/apply
the infrastructure.

If you have the `gcloud` CLI installed and set to the target project id
(`gcloud config set <PROJECT_ID>`), you can enable the required APIs with the
following command:

```bash
gcloud services enable <API_NAME>
```

## Enhancements

- [ ] Provision the `Secret Manager Secret Accessor` role to the
`${var.project_id}@appspot.gserviceaccount.com` service account
