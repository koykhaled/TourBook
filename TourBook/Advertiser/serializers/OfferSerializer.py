import re
from rest_framework import serializers
from Advertiser.models.advertiser import Advertiser, Situation
from rest_framework import serializers
from Advertiser.models.offers import Offer, Offer_Attachments, OfferRequest
from django.db.models import Sum
from Advertiser.models.advertiser import AdvertiserAttachments
from Advertiser.models.service import Service


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.
    """
    class Meta:
        model = Service
        fields = ['id', 'service_field']


class AdvertiserForActiveOffersSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='user.avatar')
    id = serializers.IntegerField(source='user.id')
    service = ServiceSerializer(many=True)

    class Meta:
        model = Advertiser
        fields = ['avatar', 'place_name', 'id', 'service']


class ActiveOffersSerializer(serializers.ModelSerializer):
    advertiser = AdvertiserForActiveOffersSerializer(
        source='advertiser_object')
    service = ServiceSerializer()
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Offer
        fields = ['id', 'num_of_seat', 'start_date', 'end_date',
                  'description', 'price_for_one', 'title', 'service', 'advertiser']
