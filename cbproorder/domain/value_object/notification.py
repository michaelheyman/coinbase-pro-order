from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NotificationMessage:
    """
    A class to represent a notification message.
    """

    title: str = Field(..., description="The title of the notification.")
    contents: str = Field(..., description="The contents of the notification.")

    def to_html(self) -> str:
        """
        Convert the notification message to HTML.

        Returns:
            str: The notification message in HTML.
        """
        return f"<b>{self.title}</b>\n\n{self.contents}"

    def to_markdown(self) -> str:
        """
        Convert the notification message to Markdown.

        Returns:
            str: The notification message in Markdown.
        """
        return f"*{self.title}*\n\n{self.contents}"
