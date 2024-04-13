from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from .serializers.TourOrganizerSerializer import TourOrganizerSerializer
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from .models.tour_organizer import TourOrganizer


class TourOrganizerView(UserViewSet):
    serializer_class = UserSerializer
    organizer_serializer_class = TourOrganizerSerializer

    def get_organizer(self, request):
        """
        Retrieve the organizer data for the authenticated user.

        This method returns the serialized data of the TourOrganizer instance associated with the authenticated user.
        It checks if all fields in the serialized data have a value (not None) and sets the data_status accordingly.

        Returns:
            Response: Serialized data of the organizer and status indicating the data_status.
        """
        user = request.user
        data_status = 0
        organizer = TourOrganizer.objects.get(user=user)
        serializer = self.organizer_serializer_class(organizer)
        if all(value is not None for value in serializer.data.values()):
            data_status = 1

        return Response({
            "data": serializer.data,
            "status": data_status
        }, status=status.HTTP_200_OK)

    def update_organizer(self, request):
        """
        Update the organizer data for the authenticated user.

        This method allows updating the user and organizer data associated with the authenticated user.
        It performs partial updates on the user and organizer instances based on the provided request data.

        Args:
            request (Request): The HTTP request containing the updated user and organizer data.
            request contain to dictionaries :
                user => contain user data [phone , email , username] for updating and send email when user change his email
                organizer => contain organizer data [address , evaluation , situation , logo]



        Returns:
            Response: Serialized data of the updated organizer or error response if validation or update fails.
        """
        try:
            user = request.user
            organizer = TourOrganizer.objects.get(user=user)
            user_serializer = self.serializer_class(user)
            organizer_serializer = self.organizer_serializer_class(organizer)

            if 'user' in request.data and request.data['user']:
                user_serializer = self.serializer_class(
                    user, data=request.data['user'], partial=True)
                user_serializer.is_valid(raise_exception=True)
                self.perform_update(user_serializer)

            if 'organizer' in request.data:
                organizer_serializer = self.organizer_serializer_class(
                    organizer, data=request.data['organizer'], partial=True)
                if not organizer_serializer.is_valid():
                    return Response({
                        'errors': organizer_serializer.errors
                    })
                organizer_serializer.save()

            if 'logo' in request.data:
                organizer_serializer = self.organizer_serializer_class(
                    organizer, data=request.data, partial=True)
                if not organizer_serializer.is_valid():
                    return Response({
                        'errors': organizer_serializer.errors
                    })
                organizer_serializer.save()

            return Response(
                {
                    'data': organizer_serializer.data,
                    'message': 'Organizer Updated Successfully'
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'error': str(e.get)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
