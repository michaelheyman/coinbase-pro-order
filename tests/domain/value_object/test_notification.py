import unittest

from cbproorder.domain.value_object.notification import NotificationMessage


class TestNotificationMessage(unittest.TestCase):
    def test_to_html(self):
        # Arrange
        title = "Test Title"
        contents = "Test Contents"
        expected_html = f"<b>{title}</b>\n\n{contents}"
        message = NotificationMessage(title=title, contents=contents)

        # Act
        actual_html = message.to_html()

        # Assert
        self.assertEqual(
            actual_html,
            expected_html,
            f"Expected '{expected_html}', but got '{actual_html}'",
        )

    def test_to_markdown(self):
        # Arrange
        title = "Test Title"
        contents = "Test Contents"
        expected_markdown = f"*{title}*\n\n{contents}"
        message = NotificationMessage(title=title, contents=contents)

        # Act
        actual_markdown = message.to_markdown()

        # Assert
        self.assertEqual(
            actual_markdown,
            expected_markdown,
            f"Expected '{expected_markdown}', but got '{actual_markdown}'",
        )
