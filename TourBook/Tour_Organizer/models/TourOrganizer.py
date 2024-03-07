from django.db import models
from django.conf import settings
import re
# Create your models here.


class Situation(models.TextChoices):
    SUBCRIEPER = "SUB", "Subscriper"
    UNSUBCRIEPER = "UNSUB", "UnSubscriper"
    BLOCKED = "B", "Blocked"

    def getSituationKeys():
        keys = [key for key, _ in Situation.choices]
        return keys


class BaseModel(models.Model):
    """A base model representing common fields for other models.

    Attributes:
        created_at (datetime): The date and time when the record was created.
        updated_at (datetime): The date and time when the record was last updated.
    """
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_char_fields(self):
        char_fields = []
        fields = self._meta.get_fields()
        for field in fields:
            if isinstance(field, models.CharField):
                char_fields.append(field)
        return char_fields

    def get_numeric_fields(self):
        numeric_fields = []
        fields = self._meta.get_fields()
        for field in fields:
            if isinstance(field, models.IntegerField) or isinstance(field, models.DecimalField):
                numeric_fields.append(field)

        return numeric_fields


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
    address = models.CharField(max_length=255)

    evaluation = models.IntegerField(default=0)

    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    situation = models.CharField(
        max_length=20, choices=Situation.choices, default=Situation.UNSUBCRIEPER)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organizer')

    def is_within(self, min_value: int, max_value: int, value: int):
        """
        Checks if a value is within a specified range.

        Args:
        - min_value (int): The minimum allowed value.
        - max_value (int): The maximum allowed value.
        - value (int): The value to check.

        Returns:
        - bool: True if the value is within the specified range, False otherwise.
        """
        return min_value <= value <= max_value

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
