from cbproorder.domain.notification_service import NotificationService
from cbproorder.domain.value_object.notification import NotificationMessage
from cbproorder.infrastructure.logger import get_logger

logger = get_logger(__name__)


class TelegramNotificationService(NotificationService):
    """
    A class to represent a Telegram notification service.

    This class sends notifications via Telegram using the provided API ID, API hash, bot name, bot token, and chat ID.
    """

    def __init__(self, bot_token: str, chat_id: int) -> None:
        """
        Initialize the TelegramNotificationService.

        Args:
            bot_token (str): The token for the Telegram bot.
            chat_id (int): The ID of the Telegram chat to send notifications to.
        """
        from telebot import TeleBot

        self.chat_id = chat_id
        self.client = TeleBot(token=bot_token)

    def send_notification(self, message: NotificationMessage) -> None:
        """
        Send a notification to the Telegram chat.

        This method sends a message to the Telegram chat with the given title and message. The title is bolded and the message is sent in HTML parse mode. Notifications are sent silently.

        Args:
            title (str): The title of the notification.
            message (str): The message to send in the notification.
        """
        self.client.send_message(
            chat_id=self.chat_id,
            text=message.to_html(),
            parse_mode="HTML",
            disable_notification=True,
        )

        logger.info(
            "Sent notification message via Telegram",
            extra={"notification_message": message},
        )
