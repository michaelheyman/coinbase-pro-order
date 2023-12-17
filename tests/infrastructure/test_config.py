import os
import unittest
from unittest.mock import patch

from cbproorder.infrastructure.config import Config


class TestConfig(unittest.TestCase):
    """
    A class to represent the unit tests for the Config class.
    """

    @patch.dict(os.environ, {"COINBASE_API_KEY": "test_api_key"}, clear=True)
    def test_coinbase_api_key(self):
        config = Config()
        self.assertEqual(config.COINBASE_API_KEY, "test_api_key")

    @patch.dict(os.environ, {"COINBASE_SECRET_KEY": "test_secret_key"}, clear=True)
    def test_coinbase_secret_key(self):
        config = Config()
        self.assertEqual(config.COINBASE_SECRET_KEY, "test_secret_key")

    @patch.dict(os.environ, {"LOGGING_LEVEL": "DEBUG"}, clear=True)
    def test_logging_level(self):
        config = Config()
        self.assertEqual(config.LOGGING_LEVEL, "DEBUG")

    @patch.dict(
        os.environ,
        {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"},
        clear=True,
    )
    def test_telegram_bot_token(self):
        config = Config()
        self.assertEqual(
            config.TELEGRAM_BOT_TOKEN, "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        )

    @patch.dict(os.environ, {"TELEGRAM_CHAT_ID": "123456789"}, clear=True)
    def test_telegram_chat_id(self):
        config = Config()
        self.assertEqual(config.TELEGRAM_CHAT_ID, 123456789)

    @patch.dict(os.environ, {"TELEGRAM_CHAT_ID": "12345abcd"}, clear=True)
    def test_telegram_chat_id_invalid_int_returns_none(self):
        config = Config()
        self.assertEqual(config.TELEGRAM_CHAT_ID, None)
