import unittest

from cbproorder.domain.value_object.deposit import DepositResult


class TestDepositResult(unittest.TestCase):
    def test_from_deposit_dict(self):
        # Arrange
        deposit = {
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

        # Act
        result = DepositResult.from_deposit_dict(deposit)

        # Assert
        self.assertEqual(result.status, "created")
        self.assertEqual(result.currency, "USD")
        self.assertEqual(result.amount, 10.0)
        self.assertEqual(result.fee, 0.00)

    def test_from_deposit_dict_ignores_none_values(self):
        # Arrange
        deposit = {
            "data": {
                "status": "created",
                "amount": {
                    "currency": "USD",
                },
            }
        }

        # Act
        result = DepositResult.from_deposit_dict(deposit)

        # Assert
        self.assertEqual(result.status, "created")
        self.assertEqual(result.currency, "USD")
        self.assertEqual(result.amount, None)
        self.assertEqual(result.fee, None)
