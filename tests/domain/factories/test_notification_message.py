import unittest

from cbproorder.domain.factories.notification_message import NotificationMessageFactory
from cbproorder.domain.value_object.notification import NotificationMessage


class TestNotificationMessageFactory(unittest.TestCase):
    def test_create_order_created_message(self):
        message = NotificationMessageFactory.create_message(
            "order_created",
            quote_size=100.0,
            pair="BTC-USD",
        )
        self.assertIsInstance(message, NotificationMessage)
        self.assertEqual(message.title, "🎉 Order Created Successfully")
        self.assertIn(
            "You've successfully created an order for $100.00 of BTC-USD",
            message.contents,
        )

    def test_create_deposit_completed_message(self):
        message = NotificationMessageFactory.create_message(
            "deposit_completed",
            amount=200.0,
            currency="USD",
        )
        self.assertIsInstance(message, NotificationMessage)
        self.assertEqual(message.title, "🎉 Deposit Completed Successfully")
        self.assertIn(
            "You've successfully deposited $200.00 USD into your account.",
            message.contents,
        )

    def test_create_invalid_message(self):
        with self.assertRaises(ValueError):
            NotificationMessageFactory.create_message("invalid_type")
