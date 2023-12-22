from abc import ABC, abstractmethod


class SecretsProvider(ABC):
    """
    Abstract base class for secrets providers.

    A secrets provider is an object that can retrieve secrets given their IDs.
    """

    @abstractmethod
    def get_secret(self, secret_id: str) -> str:
        """
        Retrieve a secret given its ID.

        Args:
            secret_id (str): The ID of the secret.

        Returns:
            str: The secret value.
        """
        pass  # pragma: no cover
