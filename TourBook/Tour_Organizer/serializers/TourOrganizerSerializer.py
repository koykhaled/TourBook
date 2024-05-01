import re
from rest_framework import serializers
from ..models.tour_organizer import Situation, TourOrganizer
from djoser.serializers import UserSerializer
from django.core.files.storage import default_storage


class TourOrganizerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TourOrganizer
        fields = ('user', 'address', 'evaluation', 'logo', 'situation')

    def validate(self, attrs):
        """
        Performs validation on the serializer fields.

        Raises:
        - serializers.ValidationError: If any of the validation conditions fail.
        """

        errors = {}
        if 'evaluation' in attrs and not is_within(0, 5, attrs['evaluation']):
            errors['evaluation'] = "Evaluation Must be between 0 and 5"

        if 'situation' in attrs and attrs['situation'] not in Situation.getSituationKeys():
            errors['situation'] = f"Situation Must be one of {' ,'.join(Situation.getSituationKeys())}"

        if 'address' in attrs and not re.match(r'^[A-Za-z0-9\s\-.,]{4,}$', attrs['address']):
            errors['address'] = "Invalid Organizer Address"

        if 'logo' in attrs:
            allowed_types = ["image/jpeg", "image/png"]
            logo_errors = {}
            if attrs['logo'].content_type not in allowed_types:
                logo_errors['type'] = "Only JPEG and PNG image files are allowed."
            max_size = 5 * 1024 * 1024  # 5MB
            if attrs['logo'].size > max_size:
                logo_errors['size'] = "The logo file size should not exceed 5MB."
            if len(logo_errors) > 0:
                errors['logo'] = logo_errors

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return attrs

    def get_user(self, obj):
        user = obj.user
        user_serializer = UserSerializer(user)
        return user_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user_data = representation.pop('user')
        user_data = {
            'id': user_data['id'],
            'username': user_data['username'],
            'phone': user_data['phone'],
            'email': user_data['email']
        }
        representation.update(user_data)
        return representation


def is_within(min_value, max_value, value):
    return min_value <= value <= max_value
