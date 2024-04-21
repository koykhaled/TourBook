import re
from rest_framework import serializers
from Advertiser.models.advertiser import Advertiser, Situation 
from Core.models.attachment import Attachment
from accounts.serializers import UserSerializer
from rest_framework import serializers
from Advertiser.models.offers import Offer, Offer_Attachments, OfferRequest
from django.db.models import Sum
from Advertiser.models.advertiser import AdvertiserAttachments
from Advertiser.models.service import Service

class AdvertiserForActiveOffersSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='user.avatar')
    id = serializers.IntegerField(source='user.id')
    class Meta:
        model = Advertiser
        fields = ['avatar', 'place_name','id']

class ActiveOffersSerializer(serializers.ModelSerializer):
    advertiser = AdvertiserForActiveOffersSerializer(source='advertiser_object')

    class Meta:
        model = Offer
        fields = ['id', 'num_of_seat', 'start_date', 'end_date', 'description', 'price_for_one', 'title', 'service', 'advertiser']