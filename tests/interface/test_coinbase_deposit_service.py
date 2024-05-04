import os
import unittest
import uuid
from unittest.mock import patch

from cbproorder.domain.exception.deposit import (
    DepositAccountNotFound,
    DepositPaymentMethodNotFound,
)
from cbproorder.interface.coinbase_deposit_service import CoinbaseDepositService


class TestCoinbaseDepositService(unittest.TestCase):
    @patch("coinbase.rest.RESTClient")
    @patch("coinbase.wallet.client.Client")
    @patch.dict(os.environ, {"COINBASE_API_BASE_URL": "http://test-url"})
    def test_init_with_env_var(self, mock_client, mock_advanced_client):
        service = CoinbaseDepositService(
            api_key="test-api-key",
            secret_key="test-secret-key",
            api_key_name="test-api-key-name",
            private_key="test-private-key",
        )
        mock_client.assert_called_once_with(
            api_key="test-api-key",
            api_secret="test-secret-key",
            base_api_uri="http://test-url",
        )
        mock_advanced_client.assert_called_once_with(
            api_key="test-api-key-name",
            api_secret="test-private-key",
            base_api_uri="http://test-url",
        )
        self.assertEqual(service.client, mock_client.return_value)

    @patch("coinbase.rest.RESTClient")
    @patch("coinbase.wallet.client.Client")
    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_env_var(self, mock_client, mock_advanced_client):
        service = CoinbaseDepositService(
            api_key="test-api-key",
            secret_key="test-secret-key",
            api_key_name="test-api-key-name",
            private_key="test-private-key",
        )
        mock_client.assert_called_once_with(
            api_key="test-api-key",
            api_secret="test-secret-key",
        )
        mock_advanced_client.assert_called_once_with(
            api_key="test-api-key-name",
            api_secret="test-private-key",
        )
        self.assertEqual(service.client, mock_client.return_value)

    @patch(
        "cbproorder.interface.coinbase_deposit_service.CoinbaseDepositService.get_ach_payment_method_id"
    )
    @patch(
        "cbproorder.interface.coinbase_deposit_service.CoinbaseDepositService.get_deposit_account_id"
    )
    @patch("coinbase.wallet.client.Client")
    def test_deposit_usd(
        self,
        mock_client,
        mock_get_deposit,
        mock_get_payment_method_id,
    ):
        # Arrange
        client = mock_client()
        mock_get_deposit.return_value = "79774f73-3838-4505-8db6-d0a7421f3dc7"
        mock_get_payment_method_id.return_value = "738e6a58-10a1-4a89-a64b-7057d5cecf27"
        client.deposit.return_value = {
            "id": "67e0eaec-07d7-54c4-a72c-2e92826897df",
            "status": "created",
            "payment_method": {
                "id": "738e6a58-10a1-4a89-a64b-7057d5cecf27",
                "resource": "payment_method",
                "resource_path": "/v2/payment-methods/738e6a58-10a1-4a89-a64b-7057d5cecf27",
            },
            "transaction": {
                "id": "441b9494-b3f0-5b98-b9b0-4d82c21c252a",
                "resource": "transaction",
                "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/transactions/441b9494-b3f0-5b98-b9b0-4d82c21c252a",
            },
            "amount": {
                "amount": "10.00",
                "currency": "USD",
            },
            "subtotal": {
                "amount": "10.00",
                "currency": "USD",
            },
            "created_at": "2015-01-31T20:49:02Z",
            "updated_at": "2015-02-11T16:54:02-08:00",
            "resource": "deposit",
            "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/deposits/67e0eaec-07d7-54c4-a72c-2e92826897df",
            "committed": True,
            "fee": {
                "amount": "0.00",
                "currency": "USD",
            },
            "payout_at": "2015-02-18T16:54:00-08:00",
        }
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        amount = 10.0
        deposit = service.deposit_usd(amount=amount)

        # Assert
        client.deposit.assert_called_once_with(
            account_id="79774f73-3838-4505-8db6-d0a7421f3dc7",
            payment_method="738e6a58-10a1-4a89-a64b-7057d5cecf27",
            amount=str(amount),
            currency=service._USD_CURRENCY,
        )
        self.assertEqual(deposit.status, "created")
        self.assertEqual(deposit.currency, "USD")
        self.assertEqual(deposit.amount, 10.0)
        self.assertEqual(deposit.fee, 0.00)

    @patch(
        "cbproorder.interface.coinbase_deposit_service.CoinbaseDepositService.get_deposit_account_id"
    )
    @patch("coinbase.wallet.client.Client")
    def test_deposit_usd_raises_deposit_account_not_found_exception(
        self,
        mock_client,
        mock_get_deposit,
    ):
        # Arrange
        client = mock_client()
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client
        mock_get_deposit.return_value = None

        # Act & Assert
        with self.assertRaises(DepositAccountNotFound):
            amount = 10.0
            service.deposit_usd(amount=amount)

    @patch(
        "cbproorder.interface.coinbase_deposit_service.CoinbaseDepositService.get_ach_payment_method_id"
    )
    @patch(
        "cbproorder.interface.coinbase_deposit_service.CoinbaseDepositService.get_deposit_account_id"
    )
    @patch("coinbase.wallet.client.Client")
    def test_deposit_usd_raises_deposit_payment_method_not_found_exception(
        self,
        mock_client,
        mock_get_deposit,
        mock_get_payment_method_id,
    ):
        # Arrange
        client = mock_client()
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client
        mock_get_deposit.return_value = "79774f73-3838-4505-8db6-d0a7421f3dc7"
        mock_get_payment_method_id.return_value = None

        # Act & Assert
        with self.assertRaises(DepositPaymentMethodNotFound):
            amount = 10.0
            service.deposit_usd(amount=amount)

    @patch("coinbase.rest.RESTClient")
    def test_get_deposit_account_id(self, mock_client):
        # Arrange
        expected_deposit_account_id = str(uuid.uuid4())
        client = mock_client()
        client.get_accounts.return_value = {
            "accounts": [
                {
                    "uuid": expected_deposit_account_id,
                    "name": "Cash (USD)",
                    "currency": "USD",
                    "available_balance": {"value": "12.34", "currency": "USD"},
                    "default": False,
                    "active": True,
                    "created_at": "1999-12-25T11:06:13.868Z",
                    "updated_at": "2014-04-01T11:25:11.959Z",
                    "deleted_at": None,
                    "type": "ACCOUNT_TYPE_FIAT",
                    "ready": True,
                    "hold": {"value": "0", "currency": "USD"},
                },
            ],
            "has_next": False,
            "cursor": "",
            "size": 1,
        }

        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, expected_deposit_account_id)

    @patch("coinbase.rest.RESTClient")
    def test_get_deposit_account_id_empty_response_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_accounts.return_value = None
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, None)

    @patch("coinbase.rest.RESTClient")
    def test_get_deposit_account_id_empty_data_response_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_accounts.return_value = {"data": []}
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, None)

    @patch("coinbase.rest.RESTClient")
    def test_get_deposit_account_id_non_fiat_accounts_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_accounts.return_value = {
            "accounts": [
                {
                    "uuid": str(uuid.uuid4()),
                    "name": "ETH Wallet",
                    "currency": "ETH",
                    "available_balance": {
                        "value": "0.00000000",
                        "currency": "ETH",
                    },
                    "default": True,
                    "active": True,
                    "created_at": "1989-02-25T13:41:04.788Z",
                    "updated_at": "1973-02-13T05:23:22.690Z",
                    "deleted_at": None,
                    "type": "ACCOUNT_TYPE_CRYPTO",
                    "ready": True,
                    "hold": {"value": "0", "currency": "ETH"},
                },
                {
                    "uuid": str(uuid.uuid4()),
                    "name": "BTC Wallet",
                    "currency": "BTC",
                    "available_balance": {
                        "value": "0.00000000",
                        "currency": "BTC",
                    },
                    "default": True,
                    "active": True,
                    "created_at": "2013-12-16T04:11:50.900Z",
                    "updated_at": "1997-08-18T05:53:57.841Z",
                    "deleted_at": None,
                    "type": "ACCOUNT_TYPE_CRYPTO",
                    "ready": True,
                    "hold": {"value": "0", "currency": "BTC"},
                },
            ],
            "has_next": False,
            "cursor": "",
            "size": 2,
        }

        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, None)

    @patch("coinbase.rest.RESTClient")
    def test_get_ach_payment_method_id(self, mock_client):
        # Arrange
        expected_payment_method_id = str(uuid.uuid4())
        client = mock_client()
        client.list_payment_methods.return_value = {
            "payment_methods": [
                {
                    "id": expected_payment_method_id,
                    "type": "ACH",
                    "name": "International Bank *****1111",
                    "currency": "USD",
                    "verified": True,
                    "allow_buy": True,
                    "allow_sell": False,
                    "allow_deposit": True,
                    "allow_withdraw": True,
                    "created_at": "1990-01-08T23:38:59Z",
                    "updated_at": "2000-12-08T13:58:54Z",
                },
            ]
        }

        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.list_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, expected_payment_method_id)

    @patch("coinbase.rest.RESTClient")
    def test_get_ach_payment_method_id_empty_response_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.list_payment_methods.return_value = None
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.list_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, None)

    @patch("coinbase.rest.RESTClient")
    def test_get_ach_payment_method_id_empty_data_response_returns_none(
        self, mock_client
    ):
        # Arrange
        client = mock_client()
        client.list_payment_methods.return_value = {"payment_methods": []}
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.list_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, None)

    @patch("coinbase.rest.RESTClient")
    def test_get_ach_payment_method_not_ach_payment_method_returns_none(
        self, mock_client
    ):
        # Arrange
        client = mock_client()
        client.list_payment_methods.return_value = {
            "payment_methods": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "COINBASE_FIAT_ACCOUNT",
                    "name": "Cash (USD)",
                    "currency": "USD",
                    "verified": True,
                    "allow_buy": True,
                    "allow_sell": True,
                    "allow_deposit": False,
                    "allow_withdraw": False,
                    "created_at": "2003-08-02T21:24:30Z",
                    "updated_at": "2013-04-09T03:04:40Z",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "APPLE_PAY",
                    "name": "Apple Pay",
                    "currency": "USD",
                    "verified": True,
                    "allow_buy": True,
                    "allow_sell": False,
                    "allow_deposit": False,
                    "allow_withdraw": False,
                    "created_at": "2007-06-01T16:43:42Z",
                    "updated_at": "1997-03-20T17:12:05Z",
                },
            ]
        }

        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.list_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, None)

    @patch("coinbase.rest.RESTClient")
    def test_get_ach_payment_deposit_not_allowed_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.list_payment_methods.return_value = {
            "payment_methods": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "ACH",
                    "name": "International Bank *****1111",
                    "currency": "USD",
                    "verified": True,
                    "allow_buy": True,
                    "allow_sell": False,
                    "allow_deposit": False,
                    "allow_withdraw": True,
                    "created_at": "1990-01-08T23:38:59Z",
                    "updated_at": "2000-12-08T13:58:54Z",
                },
            ]
        }

        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
            api_key_name="api_key_name",
            private_key="private_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.list_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, None)
