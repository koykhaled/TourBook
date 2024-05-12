from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


from ..serializers.ClientSerializer import ClientSerializer
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from Core.permissions import IsClient

from ..models.client import Client

# Create your views here.


class ClientView(UserViewSet):
    serializer_class = UserSerializer
    client_serializer_class = ClientSerializer
    permission_classes = [IsClient]

    def get_client(self, request):
        """
        Retrieve the client data for the authenticated user.

        This method returns the serialized data of the client instance associated with the authenticated user.
        It checks if all fields in the serialized data have a value (not None) and sets the data_status accordingly.

        Returns:
            Response: Serialized data of the client and status indicating the data_status.
        """
        user = request.user
        data_status = 0
        client = Client.objects.get(user=user)
        serializer = self.client_serializer_class(client)
        if all(value is not None for value in serializer.data.values()):
            data_status = 1

        return Response({
            "data": serializer.data,
            "status": data_status
        }, status=status.HTTP_200_OK)

    def update_client(self, request):
        """
        Update the client data for the authenticated user.

        This method allows updating the user and client data associated with the authenticated user.
        It performs partial updates on the user and client instances based on the provided request data.

        Args:
            request (Request): The HTTP request containing the updated user and client data.
            request contain to dictionaries :
                user => contain user data [phone , email , username] for updating and send email when user change his email
                client => contain client data [first_name,last_name,middle_name,birth_date,gender]

        Returns:
            Response: Serialized data of the updated client or error response if validation or update fails.
        """
        try:
            user = request.user
            client = user.client
            user_serializer = self.serializer_class(user)
            client_serializer = self.client_serializer_class(client)
            errors = []

            if 'user' in request.data and request.data['user']:
                user_serializer = self.serializer_class(
                    user, data=request.data['user'], partial=True)
                if not user_serializer.is_valid(raise_exception=False):
                    errors.append(user_serializer.errors)
                else:
                    self.perform_update(user_serializer)

            if 'client' in request.data:
                client_serializer = self.client_serializer_class(
                    client, data=request.data['client'], partial=True)
                if not client_serializer.is_valid(raise_exception=False):
                    errors.append(client_serializer.errors)
                else:
                    client_serializer.save()

            if 'logo' in request.data:
                client_serializer = self.client_serializer_class(
                    client, data=request.data, partial=True)
                if not client_serializer.is_valid():
                    errors.append(client_serializer.errors)
                else:
                    client_serializer.save()

            if errors:
                raise ValidationError(errors)

            return Response(
                {
                    'data': client_serializer.data,
                    'message': 'client Updated Successfully'
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
