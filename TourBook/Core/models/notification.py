from django.db import models
from .user import UserAccount
from .base import BaseModel


class Notification (BaseModel):
    """
    Model representing a notification.

    Attributes:
        content (str): The content of the notification.
        user_id (UserAccount): The user associated with the notification.
    """
    content = models.CharField(max_length=150)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE
    )
