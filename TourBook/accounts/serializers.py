import re
from djoser.serializers import UserSerializer, UserCreateSerializer, UserCreatePasswordRetypeSerializer
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

    def validate(self, attrs):
        """Perform custom validation on user registration data.

        Args:
            attrs (dict): The attribute dictionary containing the user registration data.

        Raises:
            serializers.ValidationError: If the username is invalid or password confirmation fails.
            serializers.ValidationError: If the phone number is invalid.

        Returns:
            dict: The validated attribute dictionary.

        """
        phone = attrs.get('phone')
        username = attrs.get('username')
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)

        if not re.match('^[A-z0-9\s_]{4,}$', username):
            raise serializers.ValidationError({"username": "Invalid UserName"})

        if attrs["password"] != re_password:
            raise serializers.ValidationError(
                {"password confirmation": "Password didn't Match"})
        else:
            attrs['password'] = make_password(attrs['password'])

        if not bool(re.match(r'^[0-9]{10,20}$', phone)):
            raise serializers.ValidationError(
                {"phone": "Invalid Phone, Please Enter a Valid Number!!"})

        return attrs

    class Meta(UserCreateSerializer.Meta):
        """Meta class for UserRegisterSerializer.

        Inherits from the Meta class of UserCreateSerializer.

        Attributes:
            model (User): The User model associated with the serializer.
            fields (tuple): The fields to be included in the serialized output.
            extra_kwargs (dict): Additional options for the serializer fields.

        """
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
