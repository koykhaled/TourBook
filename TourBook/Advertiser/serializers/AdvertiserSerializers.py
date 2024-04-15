import re
from rest_framework import serializers
from ..models.advertiser import Advertiser , Service, Situation
from accounts.serializers import UserSerializer

class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.
    """
    class Meta:
        model = Service
        fields = ['id','service_field']

class AdvertiserSerializers(serializers.ModelSerializer):
    """
    Serializer for the Advertiser model.
    """
    user =UserSerializer()
    service = ServiceSerializer(many=True)

    class Meta :
        model = Advertiser
        fields = ['situation','place_capacity','place_name','link','axis_x','axis_y','user','service']
        read_only_fields = ('user',)
    
    def validate(self, attrs):
        """
        Performs validation on the serializer fields.

        Raises:
        - serializers.ValidationError: If any of the validation conditions fail.
        """

        errors = {}
        if 'axis_x' in attrs and (attrs['axis_x'] < -180 or attrs['axis_x'] > 180):
            errors['axis_x'] = "Axis x must be greater than -180 and less than 180."

        if 'axis_y' in attrs and (attrs['axis_y'] < -180 or attrs['axis_y'] > 180):
            errors['axis_y'] = "Axis y must be greater than -180 and less than 180."

        if 'situation' in attrs and attrs['situation'] not in Situation.getSituationKeys():
            errors['situation'] = f"Situation Must be one of {' ,'.join(Situation.getSituationKeys())}"

        if 'place_capacity' in attrs and attrs['place_capacity'] <= 0:
            errors['place_capacity'] = " place capacity must be greater than zero."
            
        if 'avatar' in attrs:
            allowed_types = ["image/jpeg", "image/png"]
            avatar_errors = {}
            if attrs['avatar'].content_type not in allowed_types:
                avatar_errors['type'] = "Only JPEG and PNG image files are allowed."
            max_size = 5 * 1024 * 1024  # 5MB
            if attrs['avatar'].size > max_size:
                avatar_errors['size'] = "The avatar file size should not exceed 5MB."
            if len(avatar_errors) > 0:
                errors['avatar'] = avatar_errors

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
    
