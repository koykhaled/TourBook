from django.test import TestCase
from ..models.advertiser import Advertiser
from ..models.offers import Offer, OfferRequest
from Core.models.user import UserAccount
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from ..models import Service


class SetupMixin(TestCase):
    def setUp(self):
        """
        Set up the necessary objects for testing.

        - Create a UserAccount instance for testing.
        - Create a Service instance for testing.
        - Create an Advertiser instance for testing.
        - Create an Offer instance for testing.
        - Create an OfferRequest instance for testing.
        """

        self.user = UserAccount.objects.create(
            name="jesus",
            email="jesus@gamil.com",
            phone="0937884560",
            password=make_password("khaled1234")
        )

        self.service = Service.objects.create(
            service_field="khaled"
        )

        self.advertiser = Advertiser.objects.create(
            name="jesus rast",
            situation="UNSUB",
            place_capacity=140,
            place_name="Jesus Resturant",
            link="https://www.adsf.com",
            axis_x=30,
            axis_y=-43,
            user=self.user,
        )

        self.offer = Offer.objects.create(
            title="Jesus Offer",
            price_for_one=12,
            description="ma khatartesh ala balk youm tssal any??",
            start_date="2024-03-12 12:03:00",
            end_date="2024-03-13 12:03:00",
            advertiser_object=self.advertiser
        )

        self.offerRequest = OfferRequest.objects.create(
            quantity=1,
            description="ma khatartesh ala balk youm tssal any??",
            offer_object=self.offer
        )


class TestService(SetupMixin):
    def test_service(self):
        """
        Test Validation in Service Model
        """
        with self.assertRaises(ValidationError):
            self.service.full_clean()


class TestAdvertiser(SetupMixin):
    def test_advertiser(self):
        """
        Test Validation in Advertiser Model
        """
        with self.assertRaises(ValidationError):
            self.advertiser.services.add(self.service)
            self.advertiser.full_clean()
            self.advertiser.save()


class TestOffer(SetupMixin):
    def test_offer(self):
        """
        Test Validation in Offer Model
        """
        with self.assertRaises(ValidationError):
            self.offer.full_clean()


class TestOfferRequest(SetupMixin):
    def test_offer_request(self):
        """
        Test Validation in OfferRequest Model
        """
        with self.assertRaises(ValidationError):
            self.offerRequest.full_clean()
