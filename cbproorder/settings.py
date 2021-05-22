"""Application configuration."""
import os

from dotenv import load_dotenv

load_dotenv()


class CoinbaseConfig(object):
    """Coinbase configuration settings."""

    def __init__(self):
        try:
            self.api_key = os.environ["API_KEY"]
            self.api_passphrase = os.environ["API_PASSPHRASE"]
            self.api_secret = os.environ["API_SECRET"]
        except KeyError as e:
            raise EnvironmentError(
                f"The {e} environment variable needs to be set "
                "in order to authorize access to Coinbase Pro"
            ) from KeyError
