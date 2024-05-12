from rest_framework import serializers
from .TourOrganizerSerializer import TourOrganizerSerializer
from .TourAttachmentSerializer import TourAttachmentSerializer
from .TourPointSerializer import TourPointSerializer
from ..models.tour import Tour

from datetime import datetime
import re
from Core.helpers import is_within


class TourSerializer(serializers.ModelSerializer):
    tour_attachments = TourAttachmentSerializer(many=True, required=False)
    tour_organizer = TourOrganizerSerializer(read_only=True)
    status = serializers.SerializerMethodField('get_status')
    comments_num = serializers.SerializerMethodField('get_comments_num')
    tour_points = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = (
            'id',
            'title',
            'description',
            'starting_place',
            'like_counter',
            'dislike_counter',
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

        if self.instance:
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
                print(attrs.get(field))
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
        comments_num = len(tour.tour_comments.all())
        return comments_num

    def create(self, validated_data):
        tour_attachments_data = validated_data.pop('tour_attachments', [])
        tour = Tour.objects.create(**validated_data)

        for attachment_data in tour_attachments_data:
            attachment_serializer = TourAttachmentSerializer(
                data=attachment_data)
            attachment_serializer.is_valid(raise_exception=True)
            attachment_serializer.save(tour_object=tour)

        return tour

    def update(self, instance, validated_data):
        tour_attachments_data = validated_data.pop('tour_attachments', [])

        for attachment_data in tour_attachments_data:
            attachment_serializer = TourAttachmentSerializer(
                data=attachment_data)
            attachment_serializer.is_valid(raise_exception=True)
            attachment_serializer.save(tour_object=instance)

        return super().update(instance, validated_data)
