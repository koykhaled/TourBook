from ..models.offers import OfferRequest, Offer
from rest_framework import serializers
from .AdvertiserSerializers import OfferSerializer

from django.core import exceptions


class OfferRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferRequest
        fields = ['num_of_seat', 'description', 'status', 'offer_object']
        extra_kwargs = {
            "offer_object": {'write_only': True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        offer_object = attrs.get('offer_object')
        offer = Offer.objects.get(pk=offer_object.id)
        if attrs['num_of_seat'] > offer.num_of_seat:
            raise exceptions.ValidationError(
                {'num_of_seat': 'The number of seats in the offer request cannot be greater than the number of seats in the offer.'})

        return attrs
