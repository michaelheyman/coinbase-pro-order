"""Logging module."""
import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from cbproorder import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Structured logger."""

    def add_fields(self, log_record, record, message_dict):
        """Normalize the set of default set fields that is called for every log event."""
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


config = settings.Config()

logging.getLogger().setLevel(config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)
logger.setLevel(config.LOGGING_LEVEL)
logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter("%(timestamp)s %(filename)s %(level)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
