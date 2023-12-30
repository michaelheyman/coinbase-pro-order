import unittest
from unittest.mock import patch

from cbproorder.domain.value_object.notification import NotificationMessage
from cbproorder.interface.telegram_notification_service import (
    TelegramNotificationService,
)


class TestTelegramNotificationService(unittest.TestCase):
    @patch("telebot.TeleBot")
    def test_init(self, mock_client):
        bot_token = "token"
        chat_id = 123456789
        service = TelegramNotificationService(
            bot_token=bot_token,
            chat_id=chat_id,
        )
        mock_client.assert_called_once_with(token=bot_token)
        self.assertEqual(service.chat_id, chat_id)

    @patch("telebot.TeleBot")
    def test_send_notification(self, mock_client):
        bot_token = "token"
        chat_id = 123456789
        service = TelegramNotificationService(
            bot_token=bot_token,
            chat_id=chat_id,
        )
        message = NotificationMessage(
            title="test_title",
            contents="test_message",
        )
        service.send_notification(message=message)
        mock_client.return_value.send_message.assert_called_once_with(
            chat_id=chat_id,
            text=f"<b>{message.title}</b>\n{message.contents}",
            parse_mode="HTML",
            disable_notification=True,
        )
