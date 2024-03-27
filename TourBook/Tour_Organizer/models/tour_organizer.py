from django.db import models
from django.conf import settings
from Core.models.base import BaseModel

import re
# Create your models here.


class Situation(models.TextChoices):
    SUBCRIEPER = "SUB", "Subscriper"
    UNSUBCRIEPER = "UNSUB", "UnSubscriper"
    BLOCKED = "B", "Blocked"

    def getSituationKeys():
        keys = [key for key, _ in Situation.choices]
        return keys


class TourOrganizer(BaseModel):
    """
    A model representing a tour organizer.

    Attributes:
    - address (CharField): The address of the tour organizer.
    - evaluation (IntegerField): The evaluation score of the tour organizer.
    - logo (ImageField): The logo image of the tour organizer.
    - joined_at (DateTimeField): The date and time when the tour organizer joined.
    - situation (CharField): The situation of the tour organizer (choices defined in the Situation enum).
    - user (OneToOneField): The user associated with the tour organizer.

    Methods:
    - is_within(min_value, max_value, value): Checks if a value is within a specified range.
    - clean(): Performs validation on the model fields.
    - __str__(): Returns a string representation of the tour organizer.
    """
    address = models.CharField(max_length=255, null=True)

    evaluation = models.IntegerField(default=0)

    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    situation = models.CharField(
        max_length=20, choices=Situation.choices, default=Situation.UNSUBCRIEPER)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organizer')

    def clean(self):
        """
        Performs validation on the model fields.

        Raises:
        - ValueError: If any of the validation conditions fail.
        """
        if not self.is_within(0, 5, self.evaluation):
            raise ValueError("Evaluation Must be between 0 and 5")

        if self.situation not in Situation.getSituationKeys():
            raise ValueError(
                f"Situation Must be one of {' ,'.join(Situation.getSituationKeys())}")

        if not re.match(r'^[A-Za-z0-9\s\-.,]{4,}$', self.address):
            raise ValueError("Unvalid Organizer Address")

    def __str__(self):
        return "Organizer_"+self.user.name
