from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Situation(models.TextChoices):
    SUBCRIEPER = "SUB", "Subscriper"
    UNSUBCRIEPER = "UNSUB", "UnSubscriper"
    BLOCKED = "B", "Blocked"

    def getSituationKeys():
        keys = [key for key, _ in Situation.choices]
        return keys


class Advertiser(models.Model):
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

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    situation = models.CharField( choices=Situation.choices, default=Situation.UNSUBCRIEPER)
    place_capacity = models.IntegerField(max_length=6)
    place_name = models.CharField(max_length=30)
    link = models.URLField()
    axis_x = models.FloatField(max_digits=9, decimal_places=6)
    axis_y = models.FloatField(max_digits=9, decimal_places=6)
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL ,
        on_delete = models.CASCADE )
    
    def clean(self):
        """
        Performs validation on the model fields.

        Raises:
        - ValueError: If any of the validation conditions fail.
        """
        super().clean()

        if self.place_capacity < 0:
            raise ValidationError('The capacity must be greater than zero')       
        if self.situation not in Situation.getSituationKeys():
            raise ValueError(
                f"Situation Must be one of {' ,'.join(Situation.getSituationKeys())}")       
        if not (-180 <= self.axis_x <= 180):
            raise ValidationError('Invalid x coordinate value. Must be between -180 and 180.')
        if not (-90 <= self.axis_y <= 90):
            raise ValidationError('Invalid y coordinate value. Must be between -90 and 90.')
        
        def __str__(self):
            return "Advertiser_"+self.place_name

class Advertiser_Attachments(models.Model):
    """
    This class represents an attachment associated with an advertiser.
    """
    id = models.AutoField(primary_key=True)
    advertiser_id =  models.ForeignKey(
        Advertiser ,
        on_delete = models.CASCADE )
    """attachment_id = models.ForeignKey(
        Attachment ,
        on_delete = models.CASCADE )
    """



