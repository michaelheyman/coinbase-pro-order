import os

from dotenv import load_dotenv


class Config:
    """
    A class to represent the application configuration.

    This class retrieves configuration values from environment variables and provides them as properties.

    Attributes:
        API_KEY (str): The API key for the Coinbase Advanced API.
        LOGGING_LEVEL (str): The logging level for the application.
        SECRET_KEY (str): The secret key for the Coinbase Advanced API.
    """

    def __init__(self):
        """
        Constructs an instance of the Config class.

        Loads environment variables from a .env file.
        """
        load_dotenv()

    @property
    def API_KEY(self):
        """
        Get the API key for the Coinbase Advanced API.

        Returns:
            str: The API key.
        """
        return os.getenv("API_KEY")

    @property
    def LOGGING_LEVEL(self):
        """
        Get the logging level for the application.

        Returns:
            str: The logging level. If not set, defaults to 'INFO'.
        """
        return os.getenv("LOGGING_LEVEL", "INFO")

    @property
    def SECRET_KEY(self):
        """
        Get the secret key for the Coinbase Advanced API.

        Returns:
            str: The secret key.
        """
        return os.getenv("SECRET_KEY")
