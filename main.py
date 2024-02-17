import os

from pydantic import ValidationError

from cbproorder.application.use_case.command import (
    SubmitDepositCommand,
    SubmitDepositCommandUseCase,
    SubmitMarketBuyOrderCommand,
    SubmitMarketBuyOrderCommandUseCase,
)
from cbproorder.domain.secrets_provider import SecretsProvider
from cbproorder.domain.value_object.deposit import Deposit
from cbproorder.domain.value_object.orders import Order
from cbproorder.infrastructure.config import Config
from cbproorder.infrastructure.logger import get_logger
from cbproorder.interface.coinbase_advanced_service import CoinbaseAdvancedService
from cbproorder.interface.coinbase_deposit_service import CoinbaseDepositService
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


def coinbase_orders(event: dict, context: dict) -> None:
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
        # Decode the Pub/Sub message and load it into a dict
        orders_dict = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
        logger.info("Orders received", extra={"orders": orders_dict})
        # Convert orders dict into a list of Order objects, automatically validating the data
        orders = [Order.from_dict(order_dict) for order_dict in orders_dict]
    except ValidationError as e:
        logger.error(
            "Error validating orders",
            extra={"error": e},
            exc_info=True,
        )
        return
    except Exception as e:
        logger.error(
            "Failed to read in orders",
            extra={"error": e},
            exc_info=True,
        )
        return

    secrets_provider: SecretsProvider
    if os.getenv("ENVIRONMENT") == "production":
        secrets_provider = GoogleSecretsManagerProvider(
            project_id=os.getenv("GOOGLE_PROJECT_ID", "test-project-id"),
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
            product_id=str(order.pair),
            funds=order.quote_size,
        )

        try:
            order_result = use_case.create_market_buy_order(command=buy_order_command)
            logger.debug(f"Order result {order_result}")
            logger.info("Purchase successful", extra={"order": order})
        except Exception as e:
            logger.error(
                "Failed to create market buy order",
                extra={"error": e},
                exc_info=True,
            )
            continue


def coinbase_deposit(event: dict, context: dict) -> None:
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
        # Decode the Pub/Sub message and load it into a dict
        deposit_dict = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
        # Convert orders dict into a list of Order objects, automatically validating the data
        deposit = Deposit.from_dict(deposit_dict)
    except ValidationError as e:
        logger.error(
            "Error validating deposit",
            extra={"error": e},
            exc_info=True,
        )
        return
    except Exception as e:
        logger.error(
            "Failed to read in deposit request",
            extra={"error": e},
            exc_info=True,
        )
        return

    secrets_provider: SecretsProvider
    if os.getenv("ENVIRONMENT") == "production":
        secrets_provider = GoogleSecretsManagerProvider(
            project_id=os.getenv("GOOGLE_PROJECT_ID", "test-project-id"),
        )
    else:
        secrets_provider = EnvironmentSecretsProvider()

    config = Config(secrets_provider=secrets_provider)
    deposit_service = CoinbaseDepositService(
        api_key=config.COINBASE_API_KEY,
        secret_key=config.COINBASE_SECRET_KEY,
        api_key_name=config.COINBASE_TRADING_API_KEY,
        private_key=config.COINBASE_TRADING_PRIVATE_KEY,
    )
    notification_service = TelegramNotificationService(
        bot_token=config.TELEGRAM_BOT_TOKEN,
        chat_id=config.TELEGRAM_CHAT_ID,
    )
    use_case = SubmitDepositCommandUseCase(
        deposit_service=deposit_service,
        notification_service=notification_service,
    )
    deposit_command = SubmitDepositCommand(
        amount=deposit.amount,
        currency=deposit.currency,
    )

    try:
        use_case.deposit_usd(command=deposit_command)
    except Exception as e:
        logger.error(
            "Failed to deposit USD",
            extra={"error": e},
            exc_info=True,
        )
        return
