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

Coinbase Pro lacks the support for recurring transfers, which are supported by the base version of Coinbase.
This application aims to fill that void.

`coinbase-pro-order` is a fully-managed and serverless application that allows you to configure recurring purchases
through Coinbase Pro.

## Usage

### Coinbase Pro Authentication

In order to authenticate against Coinbase you will need to create and remember these three pieces of information:

- Key
- Secret
- Passphrase

Anyone with access to these values will have access to your account, so handle these values wisely.

In order to create a Coinbase API key:

1. Go to <https://pro.coinbase.com/profile/api>
1. Create a "New API Key" under your desired portfolio, usually "Default Portfolio"
1. Provide an API key nickname such as "Coinbase Pro Order Script"
1. Give the API key the following permissions:
    - `trade`: this permission is required to execute new orders
    - `view`: this permission allows to query for data
1. A passphrase should have been automatically generated, accept that value or create your own. **Store this value safely**.
1. Follow the prompts and store your API secret safely
1. The new API key value should now show up in the description of the API key. Store this value safely

More information on Coinbase Pro authentication available in their [official docs](https://docs.pro.coinbase.com/#authentication).

### Coinbase Sandbox

The Coinbase Pro sandbox is available at <https://public.sandbox.pro.coinbase.com/profile/api>.
This public sandbox is available for testing API connectivity and web trading.

Consider creating a Coinbase API key on the sandbox version of Coinbase Pro if you want to do dry-runs.

More information on Coinbase Pro sandbox available in their [official docs](https://docs.pro.coinbase.com/#sandbox).

### Create an Environment File

Create a `.env` file in the project root, and override the following variables.

| Variable       | Type         | Description                                                                      |
| -------------- | ------------ | -------------------------------------------------------------------------------- |
| API_KEY        | **Required** | The Coinbase API key name                                                        |
| API_PASSPHRASE | **Required** | The Coinbase API passphrase associated with this API key                         |
| API_SECRET     | **Required** | The Coinbase API secret for this API key                                         |
| LOGGING_LEVEL  | **Optional** | The logging level (defaults to INFO)                                             |
| ENVIRONMENT    | **Optional** | Defaults to "development". Set this to "production" to run against real Coinbase |

The `.env` file will be automatically loaded.

## Developer Setup

### Create Virtual Environment

Create a virtual environment with a supported Python version:

```bash
pyenv install 3.9.0
pyenv virtualenv 3.9.0 coinbase-pro-order-3.9.0
pyenv activate coinbase-pro-order-3.9.0
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
