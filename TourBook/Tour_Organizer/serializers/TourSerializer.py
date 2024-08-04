from rest_framework import serializers
from .TourOrganizerSerializer import TourOrganizerSerializer
from .TourAttachmentSerializer import TourAttachmentSerializer
from .TourPointSerializer import TourPointSerializer
from ..models.tour import Tour
from ..models.tour_point import TourPoint

from Advertiser.models.offers import OfferRequest

from decimal import Decimal

from datetime import datetime
import re
from Core.helpers.helpers import is_within


class TourSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField(
        'get_total_cost', read_only=True)
    tour_attachments = TourAttachmentSerializer(many=True, required=False)
    tour_organizer = TourOrganizerSerializer(read_only=True)
    status = serializers.SerializerMethodField('get_status')
    comments_num = serializers.SerializerMethodField('get_comments_num')
    tour_points = TourPointSerializer(many=True)

    class Meta:
        model = Tour
        fields = (
            'id',
            'title',
            'description',
            'starting_place',
            'reaction',
            'comments_num',
            'seat_num',
            'seat_cost',
            'transportation_cost',
            'extra_cost',
            'total_cost',
            'x_starting_place',
            'y_starting_place',
            'start_date',
            'end_date',
            'note',
            'posted',
            'posted_at',
            'tour_organizer',
            'tour_attachments',
            'status',
            'tour_points'
        )
        read_only_fields = ('total_cost', 'tour_organizer',
                            'comments_num', 'tour_points')

    def get_char_fields(self):
        char_fields = []
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.CharField):
                char_fields.append(field_name)

        return char_fields

    def get_numeric_fields(self):
        numeric_fields = []
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.IntegerField) or isinstance(field, serializers.DecimalField):
                numeric_fields.append(field_name)

        return numeric_fields

    def validate(self, attrs):
        attrs = super().validate(attrs)
        errors = {}

        if self.instance and 'posted' in attrs:
            status = self.get_status(self.instance)

            if status != 1:
                errors['status'] = "Not All Points Accepted to Post Your Tour!!"

            if self.instance.posted:
                errors['post_tour'] = "This Tour has already been posted!"

        if 'start_date' in attrs or 'end_date' in attrs:
            date_errors = []
            if attrs['start_date'] < datetime.now() or attrs['end_date'] < datetime.now():
                date_errors.append(
                    "Start Date or End Date can't be in the past")

            if attrs['start_date'] >= attrs['end_date']:
                date_errors.append("End Date can't be before Start Date!!")

            if len(date_errors) > 0:
                errors['date'] = date_errors
        for field in self.get_char_fields():
            if field in attrs:
                if not bool(re.match(r'^[A-Za-z0-9\s]{4,}$', attrs.get(field))):
                    errors[field] = f"Invalid {field}"

        for field in self.get_numeric_fields():
            if field in attrs:
                if attrs.get(field) is not None:
                    if field in ['x_starting_place', 'y_starting_place']:
                        if not is_within(-90, 180, attrs[field]):
                            errors[field] = f"{field} Must be between -90 and 180"
                    else:
                        if attrs[field] < float(0):
                            errors[field] = f"{field} Should NOT be Negative"

        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs

    def to_internal_value(self, data):
        attachments_data = data.pop('tour_attachments', [])
        self.fields['tour_attachments'] = TourAttachmentSerializer(
            many=True, required=False)
        validated_data = super().to_internal_value(data)
        validated_data['tour_attachments'] = attachments_data
        return validated_data

    def get_seat_num(self, tour):
        tour_requests = tour.tour_requests.filter(situation="A")
        reserverd_seats = 0
        for tour_request in tour_requests:
            reserverd_seats += tour_request.seat_num
        return reserverd_seats

    def get_total_cost(self, tour):
        seats_cost = (self.get_seat_num(tour) +
                      tour.seat_num) * tour.seat_cost
        total_cost = Decimal(seats_cost) + Decimal(tour.extra_cost +
                                                   tour.transportation_cost)
        tour.total_cost = total_cost
        tour.save()
        return total_cost

    def reaction_split(self, represent, instance):
        """
        Split the 'reaction' field in the serialized representation and add separate counters for 'like' and 'dislike'.

        This method takes the serialized representation of an instance and splits the 'reaction' field into separate
        counters for 'like' and 'dislike'. The counters represent the number of 'like' and 'dislike' reactions associated
        with the instance.

        Args:
            represent (dict): The serialized representation of the instance.
            instance: The instance for which the representation is being generated.

        Returns:
            None
        """
        reaction = represent.pop('reaction')
        like_counter = instance.reaction.filter(reaction=1).count()
        dislike_counter = instance.reaction.filter(reaction=0).count()
        reaction = {
            "like_counter": like_counter,
            "dislike_counter": dislike_counter
        }
        represent.update(reaction)

    def seat_num_split(self, represent, instance):
        """
        Split the 'seat_num' field in the serialized representation into 'reversed_seats' and 'available_seats'.

        This method takes the serialized representation of an instance and splits the 'seat_num' field into separate
        fields: 'reversed_seats' and 'available_seats'. 'reversed_seats' represents the reversed seat numbers, and
        'available_seats' represents the total available seats for the instance.

        Args:
            represent (dict): The serialized representation of the instance.
            instance: The instance for which the representation is being generated.

        Returns:
            None
        """
        seat_num = represent.pop('seat_num')
        seat_num = {
            'reversed_seats': self.get_seat_num(instance),
            'available_seats': instance.seat_num
        }
        represent.update(seat_num)

    def to_representation(self, instance):
        represent = super().to_representation(instance)

        self.seat_num_split(represent, instance)

        self.reaction_split(represent, instance)

        return represent

    def get_status(self, tour):
        is_accepted = 0
        if len(tour.tour_points.all()) > 0:
            is_accepted = all(
                tour_point.offer_request.status == "A"
                for tour_point in tour.tour_points.all()
            )
        return 1 if is_accepted else 0

    def get_tour_points(self, tour):
        tour_points = tour.tour_points.all()
        serializer = TourPointSerializer(tour_points, many=True)
        return serializer.data

    def get_comments_num(self, tour):
        comments_num = tour.tour_comments.count()
        return comments_num

    def create(self, validated_data):
        tour_points_data = validated_data.pop('tour_points')
        tour_attachments_data = validated_data.pop('tour_attachments', [])
        tour = self.create_tour(validated_data)
        self.create_tour_attachments(tour_attachments_data, tour)
        self.create_tour_points(tour_points_data, tour)
        return tour

    def create_tour(self, validated_data):
        return Tour.objects.create(**validated_data)

    def create_tour_attachments(self, tour_attachments_data, tour):

        for attachment_data in tour_attachments_data:
            attachment_serializer = TourAttachmentSerializer(
                data=attachment_data)
            attachment_serializer.is_valid(raise_exception=True)
            attachment_serializer.save(tour_object=tour)

    def create_tour_points(self, tour_points_data, tour):

        tour_points = []

        for tour_point_data in tour_points_data:
            offer_request_data = tour_point_data.pop('offer_request', {})
            offer_request = OfferRequest.objects.create(**offer_request_data)
            tour_point = TourPoint(
                tour_object=tour,
                offer_request=offer_request,
                **tour_point_data
            )
            tour_points.append(tour_point)

        tour.tour_points.bulk_create(tour_points)

    def update(self, instance, validated_data):
        tour_attachments_data = validated_data.pop('tour_attachments', [])

        for attachment_data in tour_attachments_data:
            attachment_serializer = TourAttachmentSerializer(
                data=attachment_data)
            attachment_serializer.is_valid(raise_exception=True)
            attachment_serializer.save(tour_object=instance)

        instance = super().update(instance, validated_data)

        return instance
