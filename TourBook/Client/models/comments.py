from django.db import models
from Core.models.base import BaseModel
from .client import Client
from Tour_Organizer.models import Tour


class Comment(BaseModel):
    """
    Represents a comment made by a client on a tour.

    Fields:
        comments_field (TextField): The content of the comment.
        client_object (ForeignKey): The associated client object for the comment.
        tour (ForeignKey): The associated tour for the comment.

    Inherits From:
        Base: The base model providing common fields and functionality.

    """
    comments_field = models.TextField(max_length=255, default=' ')
    client_object = models.ForeignKey(Client, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)


# Sentiment Analaisys
