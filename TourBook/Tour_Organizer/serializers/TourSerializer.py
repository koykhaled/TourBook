from rest_framework import serializers
from .TourOrganizerSerializer import TourOrganizerSerializer
from .TourAttachmentSerializer import TourAttachmentSerializer
from ..models.tour import Tour

from datetime import datetime
import re


class TourSerializer(serializers.ModelSerializer):
    tour_attachments = TourAttachmentSerializer(many=True, required=False)
    tour_organizer = TourOrganizerSerializer(read_only=True)
    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Tour
        fields = (
            'id',
            'title',
            'description',
            'starting_place',
            'like_counter',
            'dislike_counter',
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
            'tour_organizer',
            'tour_attachments',
            'status'
        )
        read_only_fields = ('total_cost', 'tour_organizer')

    def get_char_fields(self):
        char_fields = []
        for field in self.fields.items():
            if isinstance(field, serializers.CharField):
                char_fields.append(field)

        return char_fields

    def get_numeric_fields(self):
        numeric_fields = []
        for field in self.fields.items():
            if isinstance(field, serializers.IntegerField) or isinstance(field, serializers.DecimalField):
                numeric_fields.append(field)

        return numeric_fields

    def validate(self, attrs):
        errors = {}
        attrs = super().validate(attrs)
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
            if not bool(re.match(r'^[A-z0-9\s]{4,}$', getattr(self, field.name))):
                errors[field.name] = f"Invalid {field.name}"

        for field in self.get_numeric_fields():
            if field.name in ['x_starting_place', 'y_starting_place']:
                if not self.is_within(-90, 180, getattr(self, field.name)):
                    errors[field.name] = f"{field.name} Must be between -90 and 180"
            else:
                if getattr(self, field.name) < 0:
                    errors[field.name] = f"{field.name} Should NOT be Negative"

        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        # print(attrs)
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

        instance = super().update(instance, validated_data)
        return instance
