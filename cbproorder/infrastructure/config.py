import os

from cbproorder.domain.secrets_provider import SecretsProvider


class Config:
    """
    A class to represent the application configuration.

    This class retrieves configuration values from secrets and provides them as properties.
    """

    def __init__(self, secrets_provider: SecretsProvider):
        """
        Initialize the Config class.

        Args:
            secrets_provider (SecretsProvider): The secrets provider to use for retrieving secrets.
        """
        self.secrets_provider = secrets_provider

    @property
    def COINBASE_API_KEY(self):
        """
        Get the API key for the Coinbase Advanced API.

        Returns:
            str: The API key.
        """
        return self.secrets_provider.get_secret("COINBASE_API_KEY")

    @property
    def COINBASE_SECRET_KEY(self):
        """
        Get the secret key for the Coinbase Advanced API.

        Returns:
            str: The secret key.
        """
        return self.secrets_provider.get_secret("COINBASE_SECRET_KEY")

    @property
    def LOGGING_LEVEL(self):
        """
        Get the logging level for the application.

        Returns:
            str: The logging level. If not set, defaults to 'INFO'.
        """
        return os.getenv("LOGGING_LEVEL", "INFO")

    @property
    def TELEGRAM_BOT_TOKEN(self):
        """
        Get the token for the Telegram bot.

        Returns:
            str: The bot token.
        """
        return self.secrets_provider.get_secret("TELEGRAM_BOT_TOKEN")

    @property
    def TELEGRAM_CHAT_ID(self):
        """
        Get the ID of the Telegram chat.

        Returns:
            int: The chat ID. If the secret is not set or is not a valid integer, returns None.
        """
        chat_id = self.secrets_provider.get_secret("TELEGRAM_CHAT_ID")
        try:
            return int(chat_id)
        except ValueError:
            return None
