from django.db import models
from django.conf import settings
from .advertiser import Advertiser

class Services(models.Model):
     """
        This class represents the service that offer by the advertiser.
     """
     id = models.AutoField(primary_key=True)
     service = models.CharField(max_length=30)
 
     def getService(self):
        return self.service

class Advertiser_Services(models.Model):
    """
         This class represents the relationship between an advertiser and the services they offer.
    """
    id = models.AutoField(primary_key=True)
    advertiser_id = models.ForeignKey(
        Advertiser ,
        on_delete = models.CASCADE )
    service_id = models.ManyToManyField(
        Services ,
        on_delete = models.CASCADE
    )

    
  