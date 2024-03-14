from django.db import models
from django.conf import settings
from Core.models.base import BaseModel
from django.core.exceptions import ValidationError
from Core.models.attachment import Attachment
from .service import Service
import re
# Create your models here.


class Situation(models.TextChoices):
    SUBCRIEPER = "SUB", "Subscriper"
    UNSUBCRIEPER = "UNSUB", "UnSubscriper"
    BLOCKED = "B", "Blocked"

    def getSituationKeys():
        keys = [key for key, _ in Situation.choices]
        return keys


class Advertiser(BaseModel):
    """
    This class represents an advertiser in the system.

    Attribute:
    - name (CharField) :  The name of the advertiser.
    - place_capacity (IntegerField) :  The capacity of the advertiser's place.
    - place_name (CharField) :  The name of the advertiser's place.
    - link (URLField) : The URL link associated with the advertiser's site or account on social media.
    - axis_x (FloatField) :     The x-coordinate of the advertiser's location on the map.
    - axis_y (FloatField) :     The y-coordinate of the advertiser's location on the map.

    """

    name = models.CharField(max_length=30)
    situation = models.CharField(max_length=10,
                                 choices=Situation.choices, default=Situation.UNSUBCRIEPER)
    place_capacity = models.IntegerField(default=0)
    place_name = models.CharField(max_length=30)
    link = models.URLField(unique=True)
    axis_x = models.FloatField(max_length=9, default=0)
    axis_y = models.FloatField(max_length=9, default=0)
    service = models.ManyToManyField(Service)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def clean(self):
        """
        Performs validation on the model fields.

        Raises:
        - ValueError: If any of the validation conditions fail.
        """
        url_pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        if not bool(re.match(url_pattern, self.link)):
            raise ValueError(
                "Unvalid Link , please make sure that start with https")

        if self.situation not in Situation.getSituationKeys():
            raise ValueError(
                f"Situation Must be one of {' ,'.join(Situation.getSituationKeys())}")

        for field in self.get_numeric_fields():
            if field.name in ['axis_x', 'axis_y']:
                if not self.is_within(-180, 180, getattr(self, field.name)):
                    raise ValueError(
                        f"{field.name} Must be between -180 and 180")
            else:
                if getattr(self, field.name) < 0:
                    raise ValueError(
                        f"{field.name} Should NOT be Negative")

        def __str__(self):
            return "Advertiser_"+self.place_name


class Advertiser_Attachments(BaseModel):
    """
    This class represents an attachment associated with an advertiser.
    """
    advertiser_object = models.ForeignKey(
        Advertiser,
        on_delete=models.CASCADE)
    attachment = models.ForeignKey(
        Attachment,
        on_delete=models.CASCADE)
