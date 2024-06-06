from rest_framework import serializers
from ..models.client import Client
from accounts.serializers import UserSerializer
from ..models.client import GenderChoices
import re


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'birth_date',
            'gender',
            'user',
        )

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user)
        return serializer.data

    def to_representation(self, instance):

        represent = super().to_representation(instance)
        user_data = represent.pop('user')
        user_data = {
            'id':  user_data['id'],
            'username':  user_data['username'],
            'email':  user_data['email'],
            'phone':  user_data['phone'],
            'avatar':  user_data['avatar'],
        }
        represent.update(user_data)
        return represent

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
        if any(field in attrs for field in self.get_char_fields()):
            for field in self.get_char_fields():
                if not bool(re.match(r'^[A-Za-z\s]{4,}$', attrs[field])):
                    errors[field] = f"Invalid {field}"

        if 'birth_date' in attrs:
            if not isinstance(attrs['birth_date'], serializers.DateField):
                errors['birth_date'] = "Birth Date Should be Date"

        if 'gender' in attrs:
            if attrs['gender'] not in GenderChoices.get_values():
                errors['gender'] = f"gender is not in {GenderChoices.get_values()}"
