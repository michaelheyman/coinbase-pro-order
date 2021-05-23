"""Application configuration."""
import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class LoggingLevel(Enum):
    """Logging levels that are valid according to python-json-logger."""

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class CoinbaseConfig(object):
    """Coinbase configuration settings."""

    def __init__(self):
        """Read API variables from the environment.

        :raises EnvironmentError: Missing required API variable
        """
        try:
            self.API_KEY = os.environ["API_KEY"]
            self.API_PASSPHRASE = os.environ["API_PASSPHRASE"]
            self.API_SECRET = os.environ["API_SECRET"]
        except KeyError as e:
            raise EnvironmentError(
                f"The {e} environment variable needs to be set "
                "in order to authorize access to Coinbase Pro"
            ) from KeyError


class Config(object):
    """General configuration settings."""

    def __init__(self):
        """Read environent variables."""
        try:
            self.LOGGING_LEVEL = os.environ["LOGGING_LEVEL"]
            if self.LOGGING_LEVEL not in LoggingLevel.__members__:
                raise KeyError("Not a valid logging level")
        except KeyError:
            self.LOGGING_LEVEL = LoggingLevel.INFO.value

        self.SANDBOX_API_URL = "https://api-public.sandbox.pro.coinbase.com"
