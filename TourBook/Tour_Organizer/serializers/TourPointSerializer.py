from datetime import datetime
from rest_framework import serializers
from Tour_Organizer.models.tour_point import TourPoint
import re
from Core.helpers import is_within


class TourPointSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('get_title')
    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = TourPoint
        fields = (
            'title',
            'position',
            'description',
            'arrival_time',
            'leaving_time',
            'axis_x',
            'axis_y',
            'tour_object',
            'offer_request',
            'status'
        )
        extra_kwargs = {
            "tour_object": {
                "write_only": True
            }
        }

    def get_title(self, tour_point):
        title = tour_point.offer_request.offer_object.title
        return title

    def get_status(self, tour_point):
        status = tour_point.offer_request.status
        return status

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
        errors = {}
        """
        Validate the TourPoint attribute.

        - Check if arrival_time and leaving_time are in the future.
        - Check if leaving_time is after arrival_time.
        - Ensure axis_x and axis_y are within the specified range.
        - Ensure numeric values expect axis_x and axis_y are non-negative.
        """
        if any(['arrival_time', 'leaving_time'] in attrs):
            date_errors = []
            if attrs['arrival_time'] < datetime.now() or attrs['leaving_time'] < datetime.now():
                date_errors.append(
                    "Arrive Time or Leaving Time can't be in the past")

            if attrs['arrival_time'] >= attrs['leaving_time']:
                date_errors.append(
                    "Leaving Time can't be before Arrive Time!!")

            for field in self.get_numeric_fields():
                if attrs.get(field) is not None:
                    if field in ['axis_x', 'axis_y']:
                        if not is_within(-90, 180, attrs[field]):
                            errors[field.name] = f"{field.name} Must be between -90 and 180"
                    else:
                        if attrs[field] < 0:
                            errors[field.name] = f"{field.name} Should NOT be Negative"
        if any(self.get_char_fields() in attrs):
            for field in self.get_char_fields():
                if not bool(re.match(r'^[A-z0-9\s]{4,}$', attrs[field])):
                    errors[field.name] = f"Invalid {field.name}"

        if len(errors) > 0:
            serializers.ValidationError(errors)
        return attrs
