"""Cloud function module."""
from cbproorder import main
from cbproorder.logger import logger


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

    return main.start(orders)
