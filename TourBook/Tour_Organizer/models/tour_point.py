from datetime import datetime
from django.db import models
from Core.models.base import BaseModel
from .tour import Tour
from Advertiser.models.offers import OfferRequest


class TourPoint(BaseModel):
    """
    Represents a point in a tour.

    Attributes:
        position (int): The Arrange of the tour poin Tour of the Organizer.
        description (str): The description of the tour point (optional).
        arrival_time (datetime.time): The arrival time at the tour point.
        leaving_time (datetime.time): The leaving time from the tour point.
        axis_x (int): The X coordinate of the tour point's location.
        axis_y (int): The Y coordinate of the tour point's location.
        tour_object (Tour): The foreign key to the Tour model, specifying the tour to which this point belongs.
        offer_request (OfferRequest): The foreign key to the OfferRequest model, specifying the offer request associated with this point.
    """
    position = models.IntegerField(default=0)
    description = models.TextField(max_length=1000, blank=True, null=True)
    arrival_time = models.TimeField()
    leaving_time = models.TimeField()
    axis_x = models.IntegerField(default=0)
    axis_y = models.IntegerField(default=0)
    tour_object = models.ForeignKey(
        Tour, on_delete=models.CASCADE, related_name="tour_points")
    offer_request = models.OneToOneField(
        OfferRequest, on_delete=models.CASCADE, related_name="offer_point_request")

    def clean(self):
        """
        Validate the TourPoint instance.

        - Check if arrival_time and leaving_time are in the future.
        - Check if leaving_time is after arrival_time.
        - Ensure axis_x and axis_y are within the specified range.
        - Ensure axis_x and axis_y are non-negative.
        """
        if self.arrival_time < datetime.now().time() or self.leaving_time < datetime.now().time():
            raise ValueError(
                "Arrive Time or Leaving Time can't be in the past")

        if self.arrival_time >= self.leaving_time:
            raise ValueError("Leaving Time can't be before Arrive Time!!")

        for field in self.get_numeric_fields():
            if field.name in ['axis_x', 'axis_y']:
                if not self.is_within(-90, 180, getattr(self, field.name)):
                    raise ValueError(
                        f"{field.name} Must be between -90 and 180")
            else:
                if getattr(self, field.name) < 0:
                    raise ValueError(
                        f"{field.name} Should NOT be Negative")

    def __str__(self):
        return self.tour_object.title + " Point"
