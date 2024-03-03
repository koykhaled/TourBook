from django.test import TestCase
from Admin.models import UserAccount
from Tour_Organizer.models.TourOrganizer import TourOrganizer
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.exceptions import ValidationError


class TestModels(TestCase):

    def setUp(self):
        self.user1 = UserAccount.objects.create(
            name="khaled",
            email="khaled@gmail.com",
            phone="0937884560",
            password=make_password("kikoniko")
        )

        self.organizer1 = TourOrganizer.objects.create(
            address="hom",
            evaluation=2,
            situation="B",
            logo="test.png",
            joined_at=str(timezone.now()),
            user=self.user1
        )

    def test_organizer_values(self):
        with self.assertRaises(ValidationError):
            self.organizer1.full_clean()
