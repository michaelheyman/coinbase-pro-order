from abc import ABC, abstractmethod


class NotificationServiceInterface(ABC):
    """
    A class to represent the interface for a notification service.

    This class defines the methods that a notification service must implement.
    """

    @abstractmethod
    def send_notification(self, title: str, message: str):
        """
        Send a notification with a given message.

        This method must be overridden by subclasses.

        Args:
            title (str): The title of the notification.
            message (str): The message to send in the notification.
        """
        pass
