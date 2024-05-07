import re
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()


class UserRegisterSerializer(UserCreateSerializer):
    """Serializer class for user registration.

    Extends the UserCreateSerializer and adds extra validation for user registration data.

    Attributes:
        model (User): The User model associated with the serializer.
        fields (tuple): The fields to be included in the serialized output.
        extra_kwargs (dict): Additional options for the serializer fields.

    """

    def __init__(self, *args, **kwargs):
        """Initialize the UserRegisterSerializer.

        Adds an additional field for password confirmation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, value):
        """Perform custom validation on user registration data.

        Args:
            value (dict): The attribute dictionary containing the user registration data.

        Raises:
            serializers.ValidationError: If the username is invalid or password confirmation fails.
            serializers.ValidationError: If the phone number is invalid.

        Returns:
            dict: The validated attribute dictionary.

        """
        avatar = value.get('avatar')
        phone = value.get('phone')
        username = value.get('username')
        self.fields.pop("re_password", None)
        re_password = value.pop("re_password")
        value = super().validate(value)

        if not re.match('^[A-z0-9\s_]{4,}$', username):
            raise serializers.ValidationError(
                {"username": "Enter a valid Username"})

        if value["password"] != re_password:
            raise serializers.ValidationError(
                {"password confirmation": "Password didn't Match"})
        else:
            value['password'] = make_password(value['password'])

        if not bool(re.match(r'^[0-9]{10,20}$', phone)):
            raise serializers.ValidationError(
                {"phone": "Enter a valid Phone"})

        return value

    class Meta(UserCreateSerializer.Meta):
        """Meta class for UserRegisterSerializer.

        Inherits from the Meta class of UserCreateSerializer.

        Attributes:
            model (User): The User model associated with the serializer.
            fields (tuple): The fields to be included in the serialized output.
            extra_kwargs (dict): Additional options for the serializer fields.

        """
        model = User
        fields = ('id', 'email', 'username', 'phone',
                  'password', 'role', 'avatar')

        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'phone',
                  'password', 'role', 'avatar')
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        errors = {}
        if 'phone' in attrs and not bool(re.match(r'^[0-9]{10,20}$', attrs['phone'])):
            errors["phone"] = "Enter a valid Phone."
        attrs['username'] = self.initial_data.get(
            'username', self.instance.username)
        if not re.match(r'^[A-Za-z0-9\s\-_]{4,}$', attrs['username']):
            errors["username"] = "Enter a valid  Username."
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs
