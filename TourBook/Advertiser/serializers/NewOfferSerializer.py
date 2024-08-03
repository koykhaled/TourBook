from rest_framework import serializers
from ..models.offers import Offer
from .ServiceSerializer import ServiceSerializer
from .AdvertiserSerializers import AdvertiserSerializers
from datetime import datetime
from ..services.OfferServices import OfferValidationService
from .OfferRequestSerializer import OfferRequestSerializer


class OfferSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    advertiser_object = AdvertiserSerializers(read_only=True)
    offer_requests = OfferRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'num_of_seat', 'start_date', 'end_date',
                  'description', 'price_for_one', 'title', 'service', 'advertiser_object', 'offer_requests']

    def get_advertiser_object(self, obj):
        advertiser = obj.advertiser_object
        serializer = AdvertiserSerializers(advertiser)
        return serializer.data

    def validate(self, attrs):
        attrs = super().validate(attrs)
        errors = {}
        if 'start_date' in attrs or 'end_date' in attrs:
            date_errors = []
            if attrs['start_date'] < datetime.now() or attrs['end_date'] < datetime.now():
                date_errors.append(
                    "Start Date or End Date can't be in the past")

            if attrs['start_date'] >= attrs['end_date']:
                date_errors.append("End Date can't be before Start Date!!")

            if len(date_errors) > 0:
                errors['date'] = date_errors

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def split_advertiser(self, represent):
        advertiser_data = represent.pop('advertiser_object')
        advertiser_data = {
            "advertiser": {
                "id":  advertiser_data['id'],
                "username": advertiser_data['username'],
                "place_capacity": advertiser_data['place_capacity'],

            }
        }
        represent.update(advertiser_data)

    def split_service(self, represent):
        service_data = represent.pop('service')
        service_data = {
            "service": service_data['service_field']
        }
        represent.update(service_data)

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        self.split_advertiser(represent)
        self.split_service(represent)
        return represent

    def create(self, validated_data):
        advertiser = validated_data['advertiser_object']
        service = validated_data['service']

        OfferValidationService.service_validation(advertiser, service)

        OfferValidationService.num_of_seat_validation(
            advertiser, validated_data['num_of_seat'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        service = validated_data.pop('service', None)
        num_of_seat = validated_data.pop('num_of_seat', None)
        advertiser = instance.advertiser_object

        if num_of_seat:
            OfferValidationService.num_of_seat_validation(
                instance.advertiser_object, num_of_seat)

        if service:
            OfferValidationService.service_validation(
                advertiser, service)
            instance.service = service
        return super().update(instance, validated_data)
