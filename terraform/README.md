# terraform

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Installing Terraform](#installing-terraform)
- [Set up Google Cloud Platform](#set-up-google-cloud-platform)
- [Usage](#usage)
  - [Configuring Terraform](#configuring-terraform)
  - [Running Terraform](#running-terraform)
  - [Terraform Best-Practices](#terraform-best-practices)
    - [`tfsec`](#tfsec)
- [Troubleshooting](#troubleshooting)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installing Terraform

Install Terraform by tapping into the Terraform keg and installing the CLI via `brew`:

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

For more up-to-date information, visit the [Terraform docs](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/gcp-get-started)
on this subject.

## Set up Google Cloud Platform

Follow these instructions to set up Google Cloud Platform:

- [Create a GCP project](https://console.cloud.google.com/projectcreate)
- [Create a service account key](https://console.cloud.google.com/apis/credentials/serviceaccountkey):
  - Select the project you created in the previous step.
  - Click "Create Service Account".
  - Give it any name you like and click "Create".
  - For the Role, choose "Project -> Editor", then click "Continue".
  - Skip granting additional users access, and click "Done".

  After you create your service account, download your service account key.

  - Select your service account from the list.
  - Select the "Keys" tab.
  - In the drop down menu, select "Create new key".
  - Leave the "Key Type" as JSON.
  - Click "Create" to create the key and save the key file to your system.

For more up-to-date information, visit the [Terraform docs](https://learn.hashicorp.com/tutorials/terraform/google-cloud-platform-build)
on this subject.

## Usage

### Configuring Terraform

Create a `terraform.tfvars` file in this directory. Then, fill it with the following variables with their appropriate values:

- `project`: this value is your GCP project id
- `credentials_file`: this is the path to the service account key credentials file created above
- `purchase_orders`: although the config provides a default purchase, you're encouraged to update this as well

Example:

```terraform
credentials_file = "/path/to/your/credentials/file"
project          = "your-unique-gcp-project-id"
```

Visit the [variable configuration file](./variables.tf) to view other values that can be overridden.

### Running Terraform

Before running Terraform, you must initialize the directory:

```bash
terraform init
```

Then, you can optionally confirm that the configuration is valid:

```bash
terraform validate
```

Optionally, you can also view what infrastructure changes the Terraform configuration will apply:

```bash
terraform plan
```

Finally, to apply the Terraform configuration run the following:

```bash
terraform apply
```

If you want to revert your changes simply destroy the created resources:

```bash
terraform destroy
```

### Terraform Best-Practices

#### `tfsec`

See [official docs](https://github.com/aquasecurity/tfsec#installation) for installation instructions.

Usage:

```bash
tfsec . --tfvars-file variables.tf
```

## Troubleshooting

The Terraform config attempts to enable the required APIs, but if that doesn't work follow the descriptive
errors when attempting to plan/apply the infrastructure.

If you have the `gcloud` CLI installed and set to the target project id (`gcloud config set <PROJECT_ID>`),
you can enable the required APIs with the following commands:

```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable pubsub.googleapis.co
```
