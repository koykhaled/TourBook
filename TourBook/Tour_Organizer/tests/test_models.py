from django.test import TestCase
from Admin.models import UserAccount
from Tour_Organizer.models.TourOrganizer import TourOrganizer
from Tour_Organizer.models.Tour import Tour
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.exceptions import ValidationError


class SetupMixin(TestCase):

    def setUp(self):
        self.user1 = UserAccount.objects.create(
            name="khaled",
            email="khaled@gmail.com",
            phone="0937884560",
            password=make_password("kikoniko")
        )

        self.organizer1 = TourOrganizer.objects.create(
            address="homs",
            evaluation=2,
            situation="B",
            logo="test.png",
            joined_at=str(timezone.now()),
            user=self.user1
        )


class TestTourOrganizer(SetupMixin):
    def test_organizer_values(self):
        with self.assertRaises(ValidationError):
            self.organizer1.full_clean()


class TestTour(SetupMixin):
    def setUp(self):
        super().setUp()
        self.tour1 = Tour.objects.create(
            title='khaled',
            starting_place='khaled toure',
            start_date="2024-3-9 12:09:00",
            end_date="2024-3-10 12:09:00",
            seat_num=-2,
            tour_organizer=self.organizer1
        )

    def test_tour_vlaues(self):
        with self.assertRaises(ValidationError):
            self.tour1.full_clean()
