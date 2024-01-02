import os

from dotenv import load_dotenv

from cbproorder.domain.exception.secret import RequiredSecretNotFound
from cbproorder.domain.secrets_provider import SecretsProvider


class EnvironmentSecretsProvider(SecretsProvider):
    """
    A secrets provider that retrieves secrets from environment variables.

    This class inherits from the SecretsProvider abstract base class and implements the get_secret method.
    """

    def __init__(self) -> None:
        """
        Initialize the EnvironmentSecretsProvider.

        This method loads environment variables from a .env file if it exists.
        """
        load_dotenv()

    def get_secret(self, secret_id: str) -> str:
        """
        Retrieve a secret from the environment variables given its ID.

        This method attempts to retrieve the secret with the given ID from the environment variables.
        If the secret is not found, it raises a RequiredSecretNotFound exception.

        Args:
            secret_id (str): The ID of the secret.

        Returns:
            str: The secret value.

        Raises:
            RequiredSecretNotFound: If the secret with the given ID is not found in the environment variables.
        """
        try:
            return os.environ[secret_id]
        except KeyError:
            raise RequiredSecretNotFound(secret_id=secret_id)
