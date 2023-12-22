import os
import unittest
from unittest.mock import patch

from cbproorder.interface.environments_secrets_provider import (
    EnvironmentSecretsProvider,
)


class TestEnvironmentSecretsProvider(unittest.TestCase):
    @patch.dict(os.environ, {"TEST_SECRET": "secret_value"})
    def test_get_secret(self):
        provider = EnvironmentSecretsProvider()
        self.assertEqual(provider.get_secret("TEST_SECRET"), "secret_value")

    @patch.dict(os.environ, {"TEST_SECRET": "secret_value"})
    def test_get_secret_not_found(self):
        provider = EnvironmentSecretsProvider()
        self.assertEqual(provider.get_secret("NON_EXISTENT_SECRET"), "")
