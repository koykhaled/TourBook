from django.db import models
from .user import UserAccount


class Notification (models.Model):
    """
    Model representing a notification.

    Attributes:
        content (str): The content of the notification.
        user_id (UserAccount): The user associated with the notification.
    """
    content = models.CharField(max_length=150)
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE
    )
