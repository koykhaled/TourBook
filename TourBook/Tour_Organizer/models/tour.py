from django.db import models
from Core.models.base import BaseModel
from .tour_organizer import TourOrganizer
from datetime import datetime

import re


class Tour(BaseModel):
    """
    A model representing a tour.

    Fields:
    - title (CharField): The title of the tour.
    - description (TextField): The description of the tour.
    - starting_place (CharField): The starting place of the tour.
    - like_counter (IntegerField): The number of likes for the tour.
    - dislike_counter (IntegerField): The number of dislikes for the tour.
    - seat_num (IntegerField): The number of available seats for the tour.
    - seat_cost (DecimalField): The cost of each seat for the tour.
    - transportation_cost (DecimalField): The cost of transportation for the tour.
    - extra_cost (DecimalField): The additional cost for the tour.
    - total_cost (DecimalField): The total cost of the tour.
    - x_starting_place (IntegerField): The X-coordinate of the starting place.
    - y_starting_place (IntegerField): The Y-coordinate of the starting place.
    - start_date (DateTimeField): The start date and time of the tour (inserted by Tour Organizer).
    - end_date (DateTimeField): The end date and time of the tour (inserted by Tour Organizer).
    - note (TextField): Additional note or information about the tour.
    - tour_organizer (ForeignKey): The tour organizer associated with the tour.
    """
    title = models.CharField(max_length=100)

    description = models.TextField(max_length=1000, blank=True, null=True)

    starting_place = models.CharField(max_length=100)

    like_counter = models.IntegerField(default=0)
    dislike_counter = models.IntegerField(default=0)
    comment_counter = models.IntegerField(default=0)

    seat_num = models.IntegerField(default=0)
    seat_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    transportation_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    extra_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    x_starting_place = models.IntegerField(default=0)
    y_starting_place = models.IntegerField(default=0)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    note = models.TextField(blank=True, null=True)

    tour_organizer = models.ForeignKey(TourOrganizer, on_delete=models.CASCADE)

    @property
    def calculate_total_cost(self):
        """
        total cost is a driven field can calcualte from other fields
        property to calculate total_cost fields by sum seats , transportaion and extra cost
        """
        seats_cost = self.seat_num * self.seat_cost
        total_cost = seats_cost + self.extra_cost + self.transportation_cost
        return total_cost

    def clean(self):
        """
        Cleans and validates the model instance before saving.


        - Checks if the start_date and end_date are not in the past.
        - Ensures that the end_date is after the start_date.
        - Validates the title and other character fields.
        - Ensures that numeric fields are not Negative.
        """

        if self.start_date < datetime.now() or self.end_date < datetime.now():
            raise ValueError("Start Date or End Date can't be in the past")

        if self.start_date >= self.end_date:
            raise ValueError("End Date can't be before Start Date!!")

        for field in self.get_char_fields():
            if not bool(re.match(r'^[A-z0-9\s]{4,}$', getattr(self, field.name))):
                raise ValueError(f"Invalid {field.name  }")

        for field in self.get_numeric_fields():
            if field.name in ['x_starting_place', 'y_starting_place']:
                if not self.is_within(-90, 180, getattr(self, field.name)):
                    raise ValueError(
                        f"{field.name} Must be between -90 and 180")
            else:
                if getattr(self, field.name) < 0:
                    raise ValueError(
                        f"{field.name} Should NOT be Negative")

    def save(self, *args, **kwargs):
        self.end_date = datetime.strptime(
            str(self.end_date), "%Y-%m-%d %H:%M:%S")

        self.start_date = datetime.strptime(
            str(self.start_date), "%Y-%m-%d %H:%M:%S")

        self.total_cost = self.calculate_total_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
