import unittest
from unittest.mock import MagicMock, patch

from cbproorder.interface.google_secrets_manager_provider import (
    GoogleSecretsManagerProvider,
)


class TestGoogleSecretsManagerProvider(unittest.TestCase):
    @patch("google.cloud.secretmanager.SecretManagerServiceClient")
    def test_get_secret(self, mock_client):
        mock_response = MagicMock()
        mock_response.payload.data.decode.return_value = "secret_value"
        mock_client.return_value.access_secret_version.return_value = mock_response

        provider = GoogleSecretsManagerProvider("test_project")
        secret = provider.get_secret("TEST_SECRET")

        self.assertEqual(secret, "secret_value")
        mock_client.return_value.access_secret_version.assert_called_once_with(
            request={
                "name": "projects/test_project/secrets/test_secret/versions/latest"
            }
        )
