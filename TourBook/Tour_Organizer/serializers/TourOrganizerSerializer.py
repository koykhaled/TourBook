import re
from rest_framework import serializers
from ..models.tour_organizer import Situation, TourOrganizer
from djoser.serializers import UserSerializer
from Core.helpers import is_within


class TourOrganizerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TourOrganizer
        fields = ('user', 'address', 'evaluation', 'logo', 'situation')

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
        """
        Performs validation on the serializer fields.

        Raises:
        - serializers.ValidationError: If any of the validation conditions fail.
        """
        attrs = super().validate(attrs)
        errors = {}

        for field in self.get_char_fields():
            if field in attrs:
                if not bool(re.match(r'^[A-Za-z0-9\s\-.,]{4,}$', attrs[field])):
                    errors[field] = f"Invalid {field}"

        for field in self.get_numeric_fields():
            if field in attrs:
                if attrs.get(field) is not None:
                    if field == 'evaluation':
                        if not is_within(0, 5, attrs['evaluation']):
                            errors[field] = f"{field} Must be between -90 and 180"
                    else:
                        if attrs[field] < 0:
                            errors[field] = f"{field} Should NOT be Negative"

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
