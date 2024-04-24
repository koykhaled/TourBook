import datetime
from rest_framework import serializers
from Advertiser.models.offers import OfferRequest
from Tour_Organizer.models.tour import Tour
from Tour_Organizer.models.tour_point import TourPoint
from Tour_Organizer.models.tour_organizer import TourOrganizer

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

