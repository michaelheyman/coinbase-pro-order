import unittest
from unittest.mock import MagicMock, patch

from google.api_core.exceptions import NotFound

from cbproorder.domain.exception.secret import RequiredSecretNotFound
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

    @patch("google.cloud.secretmanager.SecretManagerServiceClient")
    def test_get_secret_should_raise_exception_when_secret_not_found(self, mock_client):
        mock_client.return_value.access_secret_version.side_effect = NotFound(
            message="404 Secret [projects/111111111111/secrets/non_existent_secret] not found or has no versions."
        )

        with self.assertRaises(RequiredSecretNotFound):
            provider = GoogleSecretsManagerProvider("test_project")
            provider.get_secret("NON_EXISTENT_SECRET")
            secret = provider.get_secret("TEST_SECRET")
            self.assertEqual(secret, "secret_value")

        mock_client.return_value.access_secret_version.assert_called_once_with(
            request={
                "name": "projects/test_project/secrets/non_existent_secret/versions/latest"
            }
        )
