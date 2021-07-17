import os
from unittest import TestCase
from unittest.mock import patch

from cbproorder import utils


class TestUtils(TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_is_local_returns_true_when_env_not_set(self):
        local = utils.is_local()

        assert local == True

    @patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True)
    def test_is_local_returns_true_when_environment_is_development(self):
        local = utils.is_local()

        assert local == True

    @patch.dict(os.environ, {"ENVIRONMENT": "local"}, clear=True)
    def test_is_local_returns_true_when_environment_is_local(self):
        local = utils.is_local()

        assert local == True

    @patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True)
    def test_is_local_returns_false_when_environment_is_set(self):
        local = utils.is_local()

        assert local == False
