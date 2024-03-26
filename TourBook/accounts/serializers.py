import re
from djoser.serializers import UserSerializer, UserCreateSerializer, UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()


class UserRegisterSerializer(UserCreatePasswordRetypeSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, attrs):
        phone = attrs.get('phone')
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)
        if attrs["password"] != re_password:
            raise serializers.ValidationError(
                {"password confirmation": "Password didn't Match"})
        else:
            attrs['password'] = make_password(attrs['password'])

        if not bool(re.match(r'^[0-9]{10,20}$', phone)):
            raise serializers.ValidationError(
                {"phone": "Invalid Phone , Please Enter a Valid Number!!"})

        return attrs

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'phone', 'password', 'role')

        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'phone', 'password', 'role')
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not bool(re.match(r'^[0-9]{10,20}$', phone)):
            raise serializers.ValidationError({"phone": "Invalid Phone"})
        super().validate(attrs=attrs)
        return attrs
