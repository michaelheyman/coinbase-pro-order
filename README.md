# coinbase-pro-order

![pre-commit-workflow](https://github.com/michaelheyman/coinbase-pro-order/actions/workflows/pre-commit.yml/badge.svg)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Overview](#overview)
- [Usage](#usage)
  - [Coinbase Pro Authentication](#coinbase-pro-authentication)
  - [Coinbase Sandbox](#coinbase-sandbox)
  - [Create an Environment File](#create-an-environment-file)
- [Developer Setup](#developer-setup)
  - [Create Virtual Environment](#create-virtual-environment)
  - [Install Requirements](#install-requirements)
  - [Install Git Hooks](#install-git-hooks)
- [Testing](#testing)
- [Google Cloud Platform Integration and Deployment](#google-cloud-platform-integration-and-deployment)

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

### Create an Environment File

Create a `.env` file in the project root, and override the following variables.

| Variable       | Type         | Description                                                                      |
| -------------- | ------------ | -------------------------------------------------------------------------------- |
| API_KEY        | **Required** | The Coinbase API key name                                                        |
| API_SECRET     | **Required** | The Coinbase API secret for this API key                                         |
| LOGGING_LEVEL  | **Optional** | The logging level (defaults to INFO)                                             |

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

- [ ] Add support for Google Secrets Manager to store API key and secret
- [ ] Create a facade on top of Coinbase API to simplify the API and rely less on concrete implemenations
