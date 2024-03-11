from django.db import models
from django.core.exceptions import ValidationError
from Core.models.base import BaseModel
from datetime import datetime
import re
from .advertiser import Advertiser
from Core.models.attachment import Attachment


class Offer(BaseModel):
    """
    This class represents an offers offered by the advertiser

    Attribute:
    - start_date (DateTimeField) : The start date and time of the offer
    - end_date (DateTimeField) : The end date and time of the offer
    - price_for_one (DecimalField) : The price for one unit of the offer.
    - title (CharField) :     The title of the offer.
    - description (CharField) : The description of the offer.
    - advertiser_id :  The advertiser associated with the offer.
                       It is a foreign key referencing the 'Advertiser' model.
    """

    title = models.CharField(max_length=50)
    price_for_one = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    description = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    advertiser_object = models.ForeignKey(
        Advertiser,
        on_delete=models.CASCADE)

    def clean(self):
        """
        Performs validation on the model fields.

        Raises:
        - ValueError: If any of the validation conditions fail.
        """
        for field in self.get_numeric_fields():
            if getattr(self, field.name) < 0:
                raise ValueError(
                    f"{field.name} Should NOT be Negative")

        if self.start_date < datetime.now() or self.end_date < datetime.now():
            raise ValueError("Start Date or End Date can't be in the past")

        if self.start_date >= self.end_date:
            raise ValueError("End Date can't be before Start Date!!")

        if not re.match(r'^[A-z0-9\s]{4,}$', self.title):
            raise ValueError(f"Invalid {self.title}")

    def save(self, *args, **kwargs):
        """
        Overrides the save method to format the start and end dates into datetime objects.
        """
        self.end_date = datetime.strptime(
            str(self.end_date), "%Y-%m-%d %H:%M:%S")

        self.start_date = datetime.strptime(
            str(self.start_date), "%Y-%m-%d %H:%M:%S")

        super().save(*args, **kwargs)


class OfferRequest(BaseModel):
    """
    This class represents an offer Request that Requsted from Organizer

    Attribute:
    - quantity (IntegerField) : The quantity for seats in the offer.
    - description (CharField) : The description of the offer request.
    - offer_object (ForeignKey) : a Foreign Key from Offer.
    """
    quantity = models.IntegerField(default=0)
    description = models.TextField(max_length=1000, blank=True, null=True)
    offer_object = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def clean(self):
        """
        Validate that no numeric field has a negative value.
        """
        for field in self.get_numeric_fields():
            if getattr(self, field.name) < 0:
                raise ValueError(
                    f"{field.name} Should NOT be Negative")


class Offer_Attachments(BaseModel):
    """
    This class represents an attachment associated with an advertiser.
    """
    offer_object = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE)
    attachment_object = models.ForeignKey(
        Attachment,
        on_delete=models.CASCADE)
