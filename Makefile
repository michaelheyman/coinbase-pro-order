CLOUD_FUNCTION_NAME=coinbase_orders
PACKAGE_NAME=cbproorder
PUBSUB_TOPIC=purchase-requests

run: ## Run the application
	python -m ${PACKAGE_NAME}

deploy: ## Deploy Cloud Function
	gcloud functions deploy ${CLOUD_FUNCTION_NAME} \
	--timeout=540 --memory=1024MB --runtime python37 \
	--trigger-topic=${PUBSUB_TOPIC} \
	--region us-central1

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

test-coverage: ## Run test coverage tool
	python -m pytest \
	--cov-report term-missing \
	--cov=${PACKAGE_NAME} tests/

test: ## Run tests
	python -m pytest -vv

.DEFAULT_GOAL := help

help:
	@grep -E '^[^: ]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
