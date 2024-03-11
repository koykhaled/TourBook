from django.test import TestCase
from  Client.models.client_request import ClientRequest
from Client.models.client import Client
from Tour_Organizer.models.TourOrganizer import TourOrganizer 
from Tour_Organizer.models.Tour import Tour
from django.core.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from Core.models import UserAccount


class TestClientRequest(TestCase):
    """
    Test case for the ClientRequest model.

    Test scenarios:
    - Test validation error when seat_num is empty.

    Setup:
    - Create UserAccount objects for tour organizers.
    - Create a TourOrganizer object.
    - Create a Tour object.
    - Create a UserAccount object for a client.
    - Create a Client object.
    - Create a ClientRequest object.

    """

    def setUp(self):
        """
        Set up the test data before running each test case.
        """
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

        self.user2 = UserAccount.objects.create(
            name="khaled1",
            email="khaled1@gmail.com",
            phone="0937884568",
            password=make_password("kikoniko")
        )

        self.client1 = Client.objects.create(
            first_name='sexs',
            middle_name='essa',
            last_name='sdasd',
            birth_date='1999-02-02',
            gender='M',
            user=self.user2
        )
        

        self.tour1 = Tour.objects.create(
             title='khaled1',
             starting_place='khaled toure1',
             start_date="2024-02-9 12:09:00",
             end_date="2024-03-10 12:09:00",
             seat_num=2,
             tour_organizer=self.organizer1
        )
        self.client_request1=ClientRequest.objects.create(
            seat_num=1,
            situation='Pnk',
            client_object=self.client1,
            tour=self.tour1
            )
    


    def test_client_request(self):
        """
        Test validation error when seat_num is empty.
        """
        with self.assertRaises(ValidationError):
            self.client_request1.full_clean() 