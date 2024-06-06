from rest_framework import serializers
from ..models.client_request import ClientRequest
from .ClientSerializer import ClientSerializer
from Tour_Organizer.serializers.TourSerializer import TourSerializer
from ..models.client_request import ClientRequest
from django.core.exceptions import ValidationError


class ClientRequestSerializer(serializers.ModelSerializer):
    client_object = ClientSerializer(read_only=True)
    tour_object = TourSerializer(read_only=True)

    class Meta:
        model = ClientRequest
        fields = (
            'id',
            'seat_num',
            'situation',
            'client_object',
            'tour_object',
        )

    def get_tour_object(self, client_request):
        tour = client_request.tour_object
        serializer = TourSerializer(tour)
        return serializer.data

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        client_data = represent.pop('client_object')
        client_data = {
            "client":  {
                "username": client_data['username'],
                "phone": client_data['phone']
            }
        }
        represent.update(client_data)
        return represent

    def validate(self, attrs):
        attrs = super().validate(attrs)

        errors = {}
        if 'seat_num' in attrs:
            if attrs['seat_num'] < 0:
                errors['seat_num'] = "number of seat Can not be Negative"
        if self.instance:
            if self.instance.situation == "A":
                errors['situation'] = "You Already Accept This request"
            tour_seat = self.instance.tour_object.seat_num
            if tour_seat < self.instance.seat_num:
                errors['seat_num'] = "Number of Requested seats is bigger than Tour Seats"

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        if ClientRequest.objects.filter(client_object=validated_data['client_object'], tour_object=validated_data['tour_object']).exists():
            raise ValidationError(
                "you already made a request for this tour.")

        if validated_data['seat_num'] > validated_data['tour_object'].seat_num:
            raise ValidationError(
                "Number of Requested seats is bigger than Tour Seats")
        return super().create(validated_data)
