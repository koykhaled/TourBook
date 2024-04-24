from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


from Tour_Organizer.models.tour_point import TourPoint
from Tour_Organizer.models.tour import Tour
from Tour_Organizer.serializers.TourPointSerializer import  TourSerializer

from .serializers.TourOrganizerSerializer import TourOrganizerSerializer
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from Core.permissions import IsOrganizer

from .models.tour_organizer import TourOrganizer

# Create your views here.


class TourOrganizerView(UserViewSet):
    serializer_class = UserSerializer
    organizer_serializer_class = TourOrganizerSerializer
    permission_classes = [IsOrganizer]

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


from rest_framework.views import APIView
from rest_framework import generics
from .models import Tour


class TourCreateView(generics.CreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer



    def create(self, request, *args, **kwargs):
        required_fields = ['user_id', 'title','end_date','start_date','y_starting_place','x_starting_place','transportation_cost','seat_cost','seat_num','starting_place']

        # Check if any required field is missing
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            response_data = {
                'message': f"Missing required fields: {', '.join(missing_fields)}"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Get the user ID from the request data
        user_id = request.data.get('user_id')

        # Check if the tour organizer exists
        try:
            tour_organizer = TourOrganizer.objects.get(id=user_id)
        except TourOrganizer.DoesNotExist:
            response_data = {
                'message': 'Tour organizer does not exist.'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Add the tour organizer to the request data
        request.data['tour_organizer'] = user_id

        # Check if a tour with the same title already exists for the tour organizer
        title = request.data.get('title')
        if Tour.objects.filter(title=title, tour_organizer=tour_organizer).exists():
            response_data = {
                'message': 'A tour with the same title already exists for the tour organizer.'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set the 'posted' field based on the default value
        posted = request.data.get('posted', False)
        serializer.save(posted=posted)

        tour_id = serializer.instance.id
        response_data = {
            'message': 'Tour created successfully.',
            'id': tour_id
        }
        return Response(response_data, status=status.HTTP_201_CREATED)