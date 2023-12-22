import os

from cbproorder.application.use_case.command import (
    SubmitMarketBuyOrderCommand,
    SubmitMarketBuyOrderCommandUseCase,
)
from cbproorder.infrastructure.config import Config
from cbproorder.infrastructure.logger import get_logger
from cbproorder.interface.coinbase_advanced_service import CoinbaseAdvancedService
from cbproorder.interface.environments_secrets_provider import (
    EnvironmentSecretsProvider,
)
from cbproorder.interface.google_secrets_manager_provider import (
    GoogleSecretsManagerProvider,
)
from cbproorder.interface.telegram_notification_service import (
    TelegramNotificationService,
)

logger = get_logger(__name__)


def coinbase_orders(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.

    Docstrings taken from: https://cloud.google.com/functions/docs/calling/pubsub

    :param event:   The dictionary with data specific to this type of event.
                    The `@type` field maps to `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                    The `data` field maps to the PubsubMessage data in a base64-encoded string.
                    The `attributes` field maps to the PubsubMessage attributes if any is present.
    :param context: The Cloud Functions event metadata. The `event_id` field
                    contains the Pub/Sub message ID. The `timestamp` field
                    contains the publish time.
                    Metadata of triggering event including `event_id` which maps to the PubsubMessage
                    messageId, `timestamp` which maps to the PubsubMessage publishTime, `event_type`
                    which maps to `google.pubsub.topic.publish`, and `resource` which is a dictionary
                    that describes the service API endpoint pubsub.googleapis.com, the triggering
                    topic's name, and the triggering event type
                    `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    :returns: None. The output is written to Cloud Logging.
    """
    import base64
    import json

    logger.info("Cloud event triggered", extra={"event": event, "context": context})

    try:
        orders = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
    except Exception as e:
        logger.error(
            "Failed to read in orders",
            extra={"error": e},
            exc_info=1,
        )
        return

    # TODO: validate orders

    if os.getenv("ENVIRONMENT") == "production":
        secrets_provider = GoogleSecretsManagerProvider(
            project_id=os.getenv("GOOGLE_PROJECT_ID"),
        )
    else:
        secrets_provider = EnvironmentSecretsProvider()

    config = Config(secrets_provider=secrets_provider)
    order_service = CoinbaseAdvancedService(
        api_key=config.COINBASE_API_KEY,
        secret_key=config.COINBASE_SECRET_KEY,
    )
    notification_service = TelegramNotificationService(
        bot_token=config.TELEGRAM_BOT_TOKEN,
        chat_id=config.TELEGRAM_CHAT_ID,
    )
    use_case = SubmitMarketBuyOrderCommandUseCase(
        order_service=order_service,
        notification_service=notification_service,
    )

    for order in orders:
        buy_order_command = SubmitMarketBuyOrderCommand(
            product_id=order["product_id"],
            funds=order["price"],
        )

        try:
            order_result = use_case.create_market_buy_order(command=buy_order_command)
            logger.debug(f"Order result {order_result}")
        except Exception as e:
            logger.error(
                "Failed to create market buy order",
                extra={"error": e},
                exc_info=1,
            )
            continue

        logger.info("Purchase successful", extra={"order": order})
