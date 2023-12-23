from google.api_core.exceptions import NotFound
from google.cloud import secretmanager

from cbproorder.domain.exception.secret import RequiredSecretNotFound
from cbproorder.domain.secrets_provider import SecretsProvider


class GoogleSecretsManagerProvider(SecretsProvider):
    """
    A secrets provider that retrieves secrets from Google Secret Manager.

    This class inherits from the SecretsProvider abstract base class and implements the get_secret method.
    """

    def __init__(self, project_id: str):
        """
        Initialize the GoogleSecretsManagerProvider.

        Args:
            project_id (str): The ID of the Google Cloud project.

        This method creates a SecretManagerServiceClient instance that will be used to access the secrets.
        """
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str) -> str:
        """
        Retrieve a secret from Google Secret Manager given its ID.

        Args:
            secret_id (str): The ID of the secret.

        Returns:
            str: The secret value.
        """
        name = f"projects/{self.project_id}/secrets/{secret_id.lower()}/versions/latest"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except NotFound:
            raise RequiredSecretNotFound(secret_id=secret_id)
