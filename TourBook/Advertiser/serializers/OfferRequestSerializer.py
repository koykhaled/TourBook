from ..models.offers import OfferRequest, Offer
from rest_framework import serializers
from .AdvertiserSerializers import OfferSerializer
from Tour_Organizer.serializers.TourOrganizerSerializer import TourOrganizerSerializer

from django.core import exceptions


class OfferRequestSerializer(serializers.ModelSerializer):
    organizer = serializers.SerializerMethodField()

    class Meta:
        model = OfferRequest
        fields = ['num_of_seat', 'description',
                  'status', 'offer_object', 'organizer']
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

    def get_organizer(self, obj):
        if hasattr(obj, 'offer_point') and obj.offer_point is not None:
            tour_point = obj.offer_point
            organizer = tour_point.tour_object.tour_organizer
            organizer = {
                "organizer_name": organizer.user.username
            }
            return organizer
        else:
            return None

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        organizer_data = represent.pop('organizer', None)
        if organizer_data:
            represent.update(organizer_data)
        return represent
