import os

from dotenv import load_dotenv


class Config:
    """
    A class to represent the application configuration.

    This class retrieves configuration values from environment variables and provides them as properties.

    Attributes:
        COINBASE_API_KEY (str): The API key for the Coinbase Advanced API.
        COINBASE_SECRET_KEY (str): The secret key for the Coinbase Advanced API.
        LOGGING_LEVEL (str): The logging level for the application.
        TELEGRAM_API_ID (str): The API ID for the Telegram API.
        TELEGRAM_API_HASH (str): The API hash for the Telegram API.
        TELEGRAM_BOT_NAME (str): The name of the Telegram bot.
        TELEGRAM_BOT_TOKEN (str): The token for the Telegram bot.
    """

    def __init__(self):
        """
        Constructs an instance of the Config class.

        Loads environment variables from a .env file.
        """
        load_dotenv()

    @property
    def COINBASE_API_KEY(self):
        """
        Get the API key for the Coinbase Advanced API.

        Returns:
            str: The API key.
        """
        return os.getenv("COINBASE_API_KEY")

    @property
    def COINBASE_SECRET_KEY(self):
        """
        Get the secret key for the Coinbase Advanced API.

        Returns:
            str: The secret key.
        """
        return os.getenv("COINBASE_SECRET_KEY")

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
        return os.getenv("TELEGRAM_BOT_TOKEN")

    @property
    def TELEGRAM_CHAT_ID(self):
        """
        Get the ID of the Telegram chat.

        Returns:
            int: The chat ID. If the environment variable is not set or is not a valid integer, returns None.
        """
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        try:
            return int(chat_id)
        except (TypeError, ValueError):
            return None
