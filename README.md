# coinbase-pro-order

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
  - [Create Google Cloud Project](#create-google-cloud-project)
    - [Browser](#browser)
    - [GCloud CLI](#gcloud-cli)
  - [Create PubSub Topic](#create-pubsub-topic)
  - [Deploy Cloud Function](#deploy-cloud-function)
  - [Schedule Recurring Job](#schedule-recurring-job)

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

1. Go to https://pro.coinbase.com/profile/api
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

The Coinbase Pro sandbox is available at https://public.sandbox.pro.coinbase.com/profile/api.
This public sandbox is available for testing API connectivity and web trading.

Consider creating a Coinbase API key on the sandbox version of Coinbase Pro if you want to do dry-runs.

More information on Coinbase Pro sandbox available in their [official docs](https://docs.pro.coinbase.com/#sandbox).

### Create an Environment File

Create a `.env` file in the project root, and override the following variables.

| Variable       | Type         | Description                                                      |
| -------------- | ------------ | ---------------------------------------------------------------- |
| API_KEY        | **Required** | The Coinbase API key name                                        |
| API_PASSPHRASE | **Required** | The Coinbase API passphrase associated with this API key         |
| API_SECRET     | **Required** | The Coinbase API secret for this API key                         |
| LOGGING_LEVEL  | **Optional** | The logging level (defaults to INFO)                             |
| SANDBOX        | **Optional** | True if running the service in sandbox mode, undefined otherwise |

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

The `gcloud` CLI is recommended for this process. You can find installation instructions in:

1. [This `brew` formula](https://formulae.brew.sh/cask/google-cloud-sdk)
1. [The official docs](https://cloud.google.com/sdk/docs/install)

### Create Google Cloud Project

More information on creating projects available in the [official docs](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

#### Browser

If you're signed into your GCP account, you can create a new project [here](https://console.cloud.google.com/projectcreate).

Otherwise:

1. Navigate to [Google Cloud Platform](https://console.cloud.google.com/) and
1. Click the projects dropdown and select "New Project"
1. Follow the prompts and take note of the project id

#### GCloud CLI

Project IDs are unique across all Google Cloud projects. Make sure your project ID is unique enough,
otherwise you may see the following error:

> ERROR: (gcloud.projects.create) Project creation failed. The project ID you specified is already in use by another project. Please try an alternative ID.

A common technique to create unique projects is to use your organization or name as a prefix.

```bash
gcloud projects create <project-id> --name="coinbase"
```

### Create PubSub Topic

[PubSub](https://cloud.google.com/pubsub/docs/overview) is a messaging service that will receive messages and produce
events that will trigger your Cloud Function. A topic is a resource that accepts and routes messages.

For the following steps, ensure that your project is the active project in your `gcloud` config:

```bash
gcloud config set project <project-id>
```

The topic name must match the topic name defined in the [Makefile](./Makefile). In this case, create the following topic:

```bash
gcloud pubsub topics create purchase-requests
```

### Deploy Cloud Function

Once the topic is configured in your project, you should be ready to deploy your Cloud Function.

Run the following commands to enable required APIs:

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
```

Simply run `make deploy` to deploy the function and associate it with the aforementioned topic.


### Schedule Recurring Job

Use Cloud Scheduler to schedule a cron job that will send a message to PubSub that will then trigger the Cloud Function.

Follow [these instructions](https://cloud.google.com/scheduler/docs/quickstart#create_a_job) to create a job and:

* Name the job something self-documenting, like "coinbase-recurrent-buy"
* Set the frequency to whatever fits your need. See [CronMaker](http://www.cronmaker.com) and [crontab.guru](https://crontab.guru/)
for assistance in creating and decoding cron expressions. Note that cron does not support an expression that triggers
"every two weeks"; for that use-case you will likely have to configure two jobs.
* For the target type, select PubSub and the topic name you created earlier. In the message body, submit something
similar to the following:
    ```json
    [{"product_id": "BTC-USD", "price": "25.0"}]
    ```
* Click "Create" to finish scheduling the job. You may choose to click "Run Now" and trigger the job immediately.
