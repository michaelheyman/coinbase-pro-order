import logging
import os
from datetime import datetime
from functools import lru_cache

from pythonjsonlogger import jsonlogger

from cbproorder.infrastructure.config import Config
from cbproorder.interface.environments_secrets_provider import (
    EnvironmentSecretsProvider,
)


@lru_cache(maxsize=None)
def config_cached() -> Config:
    """
    Get an instance of the Config class.

    This function creates an instance of the Config class, which provides application configuration. The instance is cached, so it's only created once.

    Returns:
        Config: An instance of the Config class.
    """
    return Config(secrets_provider=EnvironmentSecretsProvider())


@lru_cache(maxsize=None)
def use_standard_logging() -> str:
    """
    Check if the application should use standard logging.

    This function checks if the "ENABLE_STANDARD_LOG_FORMAT" environment variable is set. The result is cached, so the environment variable is only checked once.

    Returns:
        str: The value of the "ENABLE_STANDARD_LOG_FORMAT" environment variable, or None if it's not set.
    """
    return os.getenv("ENABLE_STANDARD_LOG_FORMAT", "false")


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    A class to represent a custom JSON formatter for logging.

    This class inherits from JsonFormatter and overrides the add_fields method to add custom fields to the log record.

    Attributes:
        log_record (dict): The log record to which fields are added.
        record (logging.LogRecord): The log record object.
        message_dict (dict): The dictionary of message fields.
    """

    def add_fields(
        self, log_record: dict, record: logging.LogRecord, message_dict: dict
    ) -> None:
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


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    The logger is configured based on the application configuration.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger.
    """
    config = config_cached()
    logging.getLogger().setLevel(config.LOGGING_LEVEL)
    logger = logging.getLogger(name)
    logger.setLevel(config.LOGGING_LEVEL)
    logHandler = logging.StreamHandler()

    if use_standard_logging():
        formatter = logging.Formatter(
            "%(asctime)s %(filename)s %(levelname)s %(message)s"
        )
    else:
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(filename)s %(level)s %(message)s"
        )

    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    return logger
