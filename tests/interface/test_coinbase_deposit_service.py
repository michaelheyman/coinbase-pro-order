import unittest
from unittest.mock import patch

from cbproorder.domain.exception.deposit import (
    DepositAccountNotFound,
    DepositPaymentMethodNotFound,
)
from cbproorder.interface.coinbase_deposit_service import CoinbaseDepositService


class TestCoinbaseDepositService(unittest.TestCase):
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
            "data": {
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
        }
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
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
            currency=service.USD_CURRENCY,
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
        )
        service.client = client
        mock_get_deposit.return_value = "79774f73-3838-4505-8db6-d0a7421f3dc7"
        mock_get_payment_method_id.return_value = None

        # Act & Assert
        with self.assertRaises(DepositPaymentMethodNotFound):
            amount = 10.0
            service.deposit_usd(amount=amount)

    @patch("coinbase.wallet.client.Client")
    def test_get_deposit_account_id(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_accounts.return_value = {
            "data": [
                {
                    "allow_deposits": True,
                    "allow_withdrawals": True,
                    "balance": {
                        "amount": "12.34",
                        "currency": "USD",
                    },
                    "created_at": "1999-12-25T11:06:13.868957",
                    "currency": {
                        "asset_id": "",
                        "code": "USD",
                        "color": "#0066cf",
                        "exponent": 2,
                        "name": "United States Dollar",
                        "rewards": None,
                        "slug": "",
                        "type": "fiat",
                    },
                    "id": "79774f73-3838-4505-8db6-d0a7421f3dc7",
                    "name": "Cash (USD)",
                    "primary": False,
                    "resource": "account",
                    "resource_path": "/v2/accounts/79774f73-3838-4505-8db6-d0a7421f3dc7",
                    "type": "fiat",
                    "updated_at": "2014-04-01T11:25:11.959497",
                },
            ]
        }
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, "79774f73-3838-4505-8db6-d0a7421f3dc7")

    @patch("coinbase.wallet.client.Client")
    def test_get_deposit_account_id_empty_response_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_accounts.return_value = None
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, None)

    @patch("coinbase.wallet.client.Client")
    def test_get_deposit_account_id_empty_data_response_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_accounts.return_value = {"data": []}
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, None)

    @patch("coinbase.wallet.client.Client")
    def test_get_deposit_account_id_non_usd_accounts_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_accounts.return_value = {
            "data": [
                {
                    "allow_deposits": True,
                    "allow_withdrawals": True,
                    "balance": {
                        "amount": "0.00000000",
                        "currency": "ETH",
                    },
                    "created_at": "1989-02-25T13:41:04.788568",
                    "currency": {
                        "asset_id": "31339d66-f0af-4b84-9060-96e780e765ae",
                        "code": "ETH",
                        "color": "#627EEA",
                        "exponent": 8,
                        "name": "Ethereum",
                        "rewards": None,
                        "slug": "ethereum",
                        "type": "crypto",
                    },
                    "id": "54361caf-0e6b-4b08-9439-73eba3fcbd87",
                    "name": "ETH Wallet",
                    "primary": True,
                    "resource": "account",
                    "resource_path": "/v2/accounts/54361caf-0e6b-4b08-9439-73eba3fcbd87",
                    "type": "wallet",
                    "updated_at": "1973-02-13T05:23:22.690321",
                },
                {
                    "allow_deposits": True,
                    "allow_withdrawals": True,
                    "balance": {
                        "amount": "0.00000000",
                        "currency": "BTC",
                    },
                    "created_at": "2013-12-16T04:11:50.900667",
                    "currency": {
                        "asset_id": "fd4414f2-4940-4d4a-baa2-e7b09953a6c4",
                        "code": "BTC",
                        "color": "#F7931A",
                        "exponent": 8,
                        "name": "Bitcoin",
                        "rewards": None,
                        "slug": "bitcoin",
                        "type": "crypto",
                    },
                    "id": "339a5e75-3beb-484a-b3a5-7d09675e141f",
                    "name": "BTC Wallet",
                    "primary": True,
                    "resource": "account",
                    "resource_path": "/v2/accounts/076c5fcd-6a80-5640-b3c3-ef939db4df70",
                    "type": "wallet",
                    "updated_at": "1997-08-18T05:53:57.841380",
                },
            ]
        }
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        deposit_account_id = service.get_deposit_account_id()

        # Assert
        client.get_accounts.assert_called_once()
        self.assertEqual(deposit_account_id, None)

    @patch("coinbase.wallet.client.Client")
    def test_get_ach_payment_method_id(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_payment_methods.return_value = {
            "data": [
                {
                    "allow_buy": True,
                    "allow_deposit": True,
                    "allow_sell": False,
                    "allow_withdraw": True,
                    "created_at": "1990-01-08T23:38:59.512776",
                    "currency": "USD",
                    "id": "738e6a58-10a1-4a89-a64b-7057d5cecf27",
                    "instant_buy": True,
                    "instant_sell": False,
                    "minimum_purchase_amount": {
                        "amount": "1.00",
                        "currency": "USD",
                    },
                    "name": "International Bank *****1111",
                    "primary_buy": True,
                    "primary_sell": False,
                    "resource": "payment_method",
                    "resource_path": "/v2/payment-methods/738e6a58-10a1-4a89-a64b-7057d5cecf27",
                    "type": "ach_bank_account",
                    "updated_at": "2000-12-08T13:58:54.687127",
                    "verified": True,
                },
            ]
        }
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.get_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, "738e6a58-10a1-4a89-a64b-7057d5cecf27")

    @patch("coinbase.wallet.client.Client")
    def test_get_ach_payment_method_id_empty_response_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_payment_methods.return_value = None
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.get_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, None)

    @patch("coinbase.wallet.client.Client")
    def test_get_ach_payment_method_id_empty_data_response_returns_none(
        self, mock_client
    ):
        # Arrange
        client = mock_client()
        client.get_payment_methods.return_value = {"data": []}
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.get_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, None)

    @patch("coinbase.wallet.client.Client")
    def test_get_ach_payment_method_no_primary_buy_returns_none(self, mock_client):
        # Arrange
        client = mock_client()
        client.get_payment_methods.return_value = {
            "data": [
                {
                    "allow_buy": True,
                    "allow_deposit": False,
                    "allow_sell": True,
                    "allow_withdraw": False,
                    "created_at": "2003-08-02T21:24:30.443923",
                    "currency": "USD",
                    "fiat_account": {
                        "id": "292a9a8f-669b-4040-97ea-752073aefeed",
                        "resource": "account",
                        "resource_path": "/v2/accounts/292a9a8f-669b-4040-97ea-752073aefeed",
                    },
                    "id": "6f28e78a-8b39-4ccc-b5d2-d76189b94e91",
                    "instant_buy": True,
                    "instant_sell": True,
                    "minimum_purchase_amount": {
                        "amount": "1.00",
                        "currency": "USD",
                    },
                    "name": "Cash (USD)",
                    "primary_buy": False,
                    "primary_sell": True,
                    "resource": "payment_method",
                    "resource_path": "/v2/payment-methods/6f28e78a-8b39-4ccc-b5d2-d76189b94e91",
                    "type": "fiat_account",
                    "updated_at": "2013-04-09T03:04:40.047706",
                    "verified": True,
                },
                {
                    "allow_buy": True,
                    "allow_deposit": False,
                    "allow_sell": False,
                    "allow_withdraw": False,
                    "created_at": "2007-06-01T16:43:42.665053",
                    "currency": "USD",
                    "id": "c1b80a22-7833-446f-9d47-3d9d0367be77",
                    "instant_buy": True,
                    "instant_sell": False,
                    "minimum_purchase_amount": {
                        "amount": "1.00",
                        "currency": "USD",
                    },
                    "name": "Apple Pay",
                    "primary_buy": False,
                    "primary_sell": False,
                    "resource": "payment_method",
                    "resource_path": "/v2/payment-methods/c1b80a22-7833-446f-9d47-3d9d0367be77",
                    "type": "apple_pay",
                    "updated_at": "1997-03-20T17:12:05.216975",
                    "verified": True,
                },
            ]
        }
        service = CoinbaseDepositService(
            api_key="api_key",
            secret_key="secret_key",
        )
        service.client = client

        # Act
        payment_method_id = service.get_ach_payment_method_id()

        # Assert
        client.get_payment_methods.assert_called_once()
        self.assertEqual(payment_method_id, None)
