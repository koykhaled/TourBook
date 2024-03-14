from django.db import models
from Core.models.base import BaseModel
from Core.models.attachment import Attachment
from .tour import Tour


class TourAttachment(BaseModel):
    """
    This class represents an attachment associated with an advertiser.
    """
    tour_object = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE, related_name="tour_attachments")
    attachment = models.ForeignKey(
        Attachment,
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'tour_attachments'
