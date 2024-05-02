from django.db import models
from Core.models.base import BaseModel
import re


class Service(BaseModel):
    """
       This class represents the service that offer by the advertiser.
    """
    service_field = models.CharField(max_length=30)

    def clean(self):
        """
        Validate that no Invalid String (service).
        """
        if not bool(re.match(r'^[A-z0-9\s]{4,}$', self.service_field)):
            raise ValueError(f"Invalid {self.service_field}")

    def __str__(self):
        return self.service_field
