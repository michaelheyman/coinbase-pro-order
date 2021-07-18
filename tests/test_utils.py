import os
from unittest import TestCase
from unittest.mock import patch

from cbproorder import utils


class TestUtils(TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_is_local_returns_true_when_env_not_set(self):
        local = utils.is_local()

        assert local is True

    @patch.dict(os.environ, {"ENVIRONMENT": "local"}, clear=True)
    def test_is_local_returns_true_when_environment_is_local(self):
        local = utils.is_local()

        assert local is True

    @patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True)
    def test_is_local_returns_false_when_environment_is_development(self):
        local = utils.is_local()

        assert local is False

    @patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True)
    def test_is_local_returns_false_when_environment_is_set(self):
        local = utils.is_local()

        assert local is False

    @patch.dict(os.environ, {}, clear=True)
    def test_is_dev_returns_false_when_env_not_set(self):
        local = utils.is_dev()

        assert local is False

    @patch.dict(os.environ, {"ENVIRONMENT": "dev"}, clear=True)
    def test_is_dev_returns_true_when_environment_is_dev(self):
        local = utils.is_dev()

        assert local is True

    @patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True)
    def test_is_dev_returns_true_when_environment_is_development(self):
        local = utils.is_dev()

        assert local is True

    @patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True)
    def test_is_dev_returns_false_when_environment_is_set(self):
        local = utils.is_dev()

        assert local is False

    @patch.dict(os.environ, {}, clear=True)
    def test_is_prod_returns_false_when_env_not_set(self):
        local = utils.is_prod()

        assert local is False

    @patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True)
    def test_is_prod_returns_false_when_environment_is_development(self):
        local = utils.is_prod()

        assert local is False

    @patch.dict(os.environ, {"ENVIRONMENT": "prod"}, clear=True)
    def test_is_prod_returns_true_when_environment_is_prod(self):
        local = utils.is_prod()

        assert local is True

    @patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True)
    def test_is_prod_returns_true_when_environment_is_production(self):
        local = utils.is_prod()

        assert local is True
