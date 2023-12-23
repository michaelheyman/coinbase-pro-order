import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from cbproorder.infrastructure.config import Config
from cbproorder.interface.environments_secrets_provider import (
    EnvironmentSecretsProvider,
)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    A class to represent a custom JSON formatter for logging.

    This class inherits from JsonFormatter and overrides the add_fields method to add custom fields to the log record.

    Attributes:
        log_record (dict): The log record to which fields are added.
        record (logging.LogRecord): The log record object.
        message_dict (dict): The dictionary of message fields.
    """

    def add_fields(self, log_record, record, message_dict):
        """
        Add custom fields to the log record.

        This method adds a timestamp field if it doesn't exist, and converts the level field to uppercase.

        Args:
            log_record (dict): The log record to which fields are added.
            record (logging.LogRecord): The log record object.
            message_dict (dict): The dictionary of message fields.
        """
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def get_logger(name):
    """
    Get a logger with the specified name.

    The logger is configured based on the application configuration.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger.
    """
    config = Config(secrets_provider=EnvironmentSecretsProvider())
    logging.getLogger().setLevel(config.LOGGING_LEVEL)
    logger = logging.getLogger(name)
    logger.setLevel(config.LOGGING_LEVEL)
    logHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter("%(timestamp)s %(filename)s %(level)s %(message)s")
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    return logger
