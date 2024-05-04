import os
import unittest
from unittest.mock import MagicMock, patch

from cbproorder.infrastructure.config import Config


class TestConfig(unittest.TestCase):
    """
    A class to represent the unit tests for the Config class.
    """

    def setUp(self):
        self.mock_secrets_provider = MagicMock()
        self.config = Config(self.mock_secrets_provider)

    def test_coinbase_api_key(self):
        self.mock_secrets_provider.get_secret.return_value = "test_api_key"
        self.assertEqual(self.config.COINBASE_API_KEY, "test_api_key")
        self.mock_secrets_provider.get_secret.assert_called_once_with(
            "COINBASE_API_KEY"
        )

    def test_coinbase_secret_key(self):
        self.mock_secrets_provider.get_secret.return_value = "test_secret_key"
        self.assertEqual(self.config.COINBASE_SECRET_KEY, "test_secret_key")
        self.mock_secrets_provider.get_secret.assert_called_once_with(
            "COINBASE_SECRET_KEY"
        )

    def test_coinbase_trading_api_key(self):
        self.mock_secrets_provider.get_secret.return_value = "test_trading_api_key"
        self.assertEqual(self.config.COINBASE_TRADING_API_KEY, "test_trading_api_key")
        self.mock_secrets_provider.get_secret.assert_called_once_with(
            "COINBASE_TRADING_API_KEY"
        )

    def test_coinbase_trading_private_key(self):
        self.mock_secrets_provider.get_secret.return_value = "test_trading_private_key"
        self.assertEqual(
            self.config.COINBASE_TRADING_PRIVATE_KEY, "test_trading_private_key"
        )
        self.mock_secrets_provider.get_secret.assert_called_once_with(
            "COINBASE_TRADING_PRIVATE_KEY"
        )

    @patch.dict(os.environ, {"LOGGING_LEVEL": "DEBUG"}, clear=True)
    def test_logging_level(self):
        self.assertEqual(self.config.LOGGING_LEVEL, "DEBUG")

    def test_logging_level_default(self):
        os.environ.pop("LOGGING_LEVEL", None)
        self.assertEqual(self.config.LOGGING_LEVEL, "INFO")

    def test_telegram_bot_token(self):
        self.mock_secrets_provider.get_secret.return_value = (
            "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        )
        self.assertEqual(
            self.config.TELEGRAM_BOT_TOKEN, "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        )
        self.mock_secrets_provider.get_secret.assert_called_once_with(
            "TELEGRAM_BOT_TOKEN"
        )

    def test_telegram_chat_id(self):
        self.mock_secrets_provider.get_secret.return_value = "123456789"
        self.assertEqual(self.config.TELEGRAM_CHAT_ID, 123456789)
        self.mock_secrets_provider.get_secret.assert_called_once_with(
            "TELEGRAM_CHAT_ID"
        )

    def test_telegram_chat_id_invalid_int_raises_exception(self):
        self.mock_secrets_provider.get_secret.return_value = "12345abcd"

        with self.assertRaises(ValueError):
            self.config.TELEGRAM_CHAT_ID
