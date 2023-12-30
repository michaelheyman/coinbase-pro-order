from abc import ABC, abstractmethod

from cbproorder.domain.value_object.notification import NotificationMessage


class NotificationService(ABC):
    """
    A class to represent the interface for a notification service.

    This class defines the methods that a notification service must implement.
    """

    @abstractmethod
    def send_notification(self, message: NotificationMessage):
        """
        Send a notification with a given message.

        This method must be overridden by subclasses.

        Args:
            message (NotificationMessage): The message to send in the notification.
        """
        pass  # pragma: no cover
