# coinbase-pro-order

![pre-commit-workflow](https://github.com/michaelheyman/coinbase-pro-order/actions/workflows/pre-commit.yml/badge.svg)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Overview](#overview)
- [Usage](#usage)
  - [Coinbase Advanced Trade API Authentication](#coinbase-advanced-trade-api-authentication)
  - [Notification Configuration](#notification-configuration)
  - [Create an Environment File](#create-an-environment-file)
- [Developer Setup](#developer-setup)
  - [Create Virtual Environment](#create-virtual-environment)
  - [Install Requirements](#install-requirements)
  - [Install Git Hooks](#install-git-hooks)
  - [Run Application Locally](#run-application-locally)
- [Testing](#testing)
- [Google Cloud Platform Integration and Deployment](#google-cloud-platform-integration-and-deployment)
- [Enhancements](#enhancements)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Overview

Coinbase lacks the support for low-fee recurring purchases, which are supported
by the base version of Coinbase. However, the base version of Coinbase lacks
charges a flat fee for each transaction based on its value:

| Total Transaction Amount                     | USD Fee                               |
| -------------------------------------------- | ------------------------------------- |
| $10 or less                                  | $0.99                                 |
| More than $10 but less than or equal to $25  | $1.49                                 |
| More than $25 but less than or equal to $50  | $1.99                                 |
| More than $50 but less than or equal to $200 | $2.99                                 |
| More than $200                               | 1.49% of the total transaction amount |

This application allows users to configure recurring purchases leveraging
Coinbase Advanced Trade API, which charges much lower fees.

`coinbase-pro-order` is a fully-managed and serverless application that allows
you to configure recurring purchases through Coinbase Advanced Trade API.

## Usage

### Coinbase Advanced Trade API Authentication

In order to authenticate against Coinbase you will need to create and remember
these three pieces of information:

- Key
- Secret

Anyone with access to these values will have access to your account, so handle
these values wisely.

In order to create a Coinbase API key:

1. Go to <https://www.coinbase.com/settings/api>
1. Click "New API Key"
1. Add all the accounts that you plan on interacting with. This includes the
"Cash (USD)" account, if you're buying with USD cash.
1. Add permissions to the API key:

    - `Cash (USD)`: this permission is required to query for account balances
    - `wallet:accounts:read`: this permission is required to query for account balances
    - `wallet:buys:create`: this permission is required to create new orders
    - `wallet:orders:read`: this permission is required to query for order status
    - `wallet:transactions:read`: this permission is required to query for transaction history
    - `wallet:user:read`: this permission is required to query for user information

1. Click "Create"
1. Make a note of the API key, and API secret. **Store these values safely**.

More information on Coinbase Advanced Trace API can be found here:

- Authentication <https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-auth>
- Permissions: <https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-overview#advanced-trade-endpoints>

### Notification Configuration

This system supports notifications via Telegram. In order to configure
notifications, you will need to create a Telegram bot and retrieve your chat ID.

1. Start a chat with [`@BotFather`](https://t.me/BotFather) and type `/newbot`
2. Reply to BotFather with a name for your bot
3. Choose a username for the bot. It must be unique and end with `bot`
4. Save the HTTP API key associated with the bot
5. Start a chat with [`@myidbot`](https://t.me/myidbot) and retrieve your chat
ID number by submitting the `/start` and then the `/getid` commands
6. Start a conversation with the bot created in step #3, and type `/start`

### Create an Environment File

Create a `.env` file in the project root, and override the following variables.

| Variable            | Type         | Description                                                                      |
| ------------------- | ------------ | ------------------------------------------------- |
| COINBASE_API_KEY    | **Required** | The Coinbase API key name                         |
| COINBASE_API_SECRET | **Required** | The Coinbase API secret for this API key          |
| LOGGING_LEVEL       | **Optional** | The logging level (defaults to INFO)              |
| TELEGRAM_BOT_TOKEN  | **Required** | The Telegram bot token of the bot created earlier |
| TELEGRAM_CHAT_ID    | **Required** | The Telegram chat ID for the destination user     |

The `.env` file will be automatically loaded.

## Developer Setup

### Create Virtual Environment

Create a virtual environment with a supported Python version:

```bash
pyenv install 3.12.0
pyenv virtualenv 3.12.0 coinbase-pro-order-3.12.0
pyenv activate coinbase-pro-order-3.12.0
```

### Install Requirements

Install the development requirements:

```bash
pip -r install requirements-dev.txt
```

### Install Git Hooks

See [.pre-commit-config.yaml](.pre-commit-config.yaml) for information on which hooks are configured.

```bash
pre-commit install
pre-commit install -t pre-push
```

### Run Application Locally

:warning: This will create real orders on Coinbase. Use with caution.

With the `functions-framework` installed, you can run the application locally
by setting up a listener for the `coinbase_orders` function:

```bash
functions-framework --target=coinbase_orders --signature-type=event --debug
```

Then, create a `test_event.json` file with the array of orders.

With the listener running, you can send a test event to the function and have it read the contents of that file:

```bash
curl -L 'http://localhost:8080' \
-H 'Content-Type: application/json' \
-H 'ce-id: 123451234512345' \
-H 'ce-specversion: 1.0' \
-H 'ce-time: 2020-01-02T12:34:56.789Z' \
-H 'ce-type: google.cloud.pubsub.topic.v1.messagePublished' \
-H 'ce-source: //pubsub.googleapis.com/projects/MY-PROJECT/topics/MY-TOPIC' \
-d '{
    "message": {
        "data": "'"$(jq -c . < test_event.json | base64)"'"
    },
    "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
}'
```

## Testing

Run the unit tests and the coverage tests:

```bash
make test
make test-coverage
```

## Google Cloud Platform Integration and Deployment

The infrastructure and deployment of this project is handled by Terraform.
View the [Terraform README](./terraform/README.md) for instructions on how to
deploy this cloud function to the Google Cloud Platform.

## Enhancements

- [ ] Validate orders
- [ ] Create notification domain object
- [ ] Add support for Google Secrets Manager to store secrets
- [ ] Support overriding JSON logging to standard logging via environment variable
- [ ] Add support for other notification mechanisms
