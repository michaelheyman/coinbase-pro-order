from cbproorder.domain.value_object.notification import NotificationMessage


class NotificationMessageFactory:
    """
    A factory class for creating notification messages.
    """

    @staticmethod
    def create_message(type: str, **kwargs) -> NotificationMessage:
        """
        Create a notification message.

        Args:
            type (str): The type of message to create.
            **kwargs: Additional keyword arguments for the message.

        Returns:
            NotificationMessage: The created notification message.

        Raises:
            ValueError: If the message type is invalid.
        """
        if type == "order_created":
            return NotificationMessage(
                title="🎉 Order Created Successfully",
                contents=(
                    f"✅ You've successfully created an order for ${kwargs['quote_size']:.2f} "
                    f"of {kwargs['pair']}.\n"
                    "\n"
                    "Keep an eye on your notifications for further details regarding this transaction."
                ),
            )
        elif type == "deposit_completed":
            return NotificationMessage(
                title="🎉 Deposit Completed Successfully",
                contents=(
                    f"✅ You've successfully deposited ${kwargs['amount']:.2f} "
                    f"${kwargs['currency']} into your account."
                ),
            )
        else:
            raise ValueError(f"Invalid message type: {type}")
