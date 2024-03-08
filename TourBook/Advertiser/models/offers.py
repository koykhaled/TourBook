from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime
import re
from .advertiser import Advertiser
from Core.models.attachment import Attachment

class Offers(models.Model):
     """
     This class represents an offers offered by the advertiser

     Attribute:
     - start_date (DateTimeField) : The start date and time of the offer 
     - end_date (DateTimeField) : The end date and time of the offer 
     - price_for_one (FloatField) : The price for one unit of the offer.
     - title (CharField) :     The title of the offer.
     - description (CharField) : The description of the offer.
     - advertiser_id :  The advertiser associated with the offer.
                        It is a foreign key referencing the 'Advertiser' model.
     """

     start_date = models.DateTimeField()
     end_date = models.DateTimeField()
     price_for_one = models.FloatField(max_length=15)
     description = models.CharField(max_length=250)
     title = models.CharField(max_length=50)
     advertiser_id = models.ForeignKey(
         Advertiser ,
         on_delete = models.CASCADE )
     def clean(self):
        """
        Performs validation on the model fields.

        Raises:
        - ValueError: If any of the validation conditions fail.
        """
        if self.place_capacity < 0:
          raise ValidationError('The price must be greater than zero')
           
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
class Offer_Attachments(models.Model):
    """
    This class represents an attachment associated with an advertiser.
    """
    id = models.AutoField(primary_key=True)
    offer_id =  models.ForeignKey(
        Offers ,
        on_delete = models.CASCADE )
    attachment_id = models.ForeignKey(
        Attachment ,
        on_delete = models.CASCADE )
