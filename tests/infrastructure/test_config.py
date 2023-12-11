import os
import unittest
from unittest.mock import patch

from cbproorder.infrastructure.config import Config


class TestConfig(unittest.TestCase):
    """
    A class to represent the unit tests for the Config class.
    """

    @patch.dict(os.environ, {"API_KEY": "test_api_key"}, clear=True)
    def test_api_key(self):
        config = Config()
        self.assertEqual(config.API_KEY, "test_api_key")

    @patch.dict(os.environ, {"LOGGING_LEVEL": "DEBUG"}, clear=True)
    def test_logging_level(self):
        config = Config()
        self.assertEqual(config.LOGGING_LEVEL, "DEBUG")

    @patch.dict(os.environ, {"SECRET_KEY": "test_secret_key"}, clear=True)
    def test_secret_key(self):
        config = Config()
        self.assertEqual(config.SECRET_KEY, "test_secret_key")
