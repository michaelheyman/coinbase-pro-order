import os

from dotenv import load_dotenv

from cbproorder.domain.secrets_provider import SecretsProvider


class EnvironmentSecretsProvider(SecretsProvider):
    """
    A secrets provider that retrieves secrets from environment variables.

    This class inherits from the SecretsProvider abstract base class and implements the get_secret method.
    """

    def __init__(self):
        """
        Initialize the EnvironmentSecretsProvider.

        This method loads environment variables from a .env file if it exists.
        """
        load_dotenv()

    # TODO: raise a custom exception if the secret is not found. Think about
    # adding a strict option to this method
    def get_secret(self, secret_id: str) -> str:
        """
        Retrieve a secret from the environment variables given its ID.

        Args:
            secret_id (str): The ID of the secret.

        Returns:
            str: The secret value, or an empty string if the secret is not found.
        """
        return os.getenv(secret_id, "")
