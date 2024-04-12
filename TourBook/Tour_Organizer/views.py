from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from .serializers.TourOrganizerSerializer import TourOrganizerSerializer
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from .models.tour_organizer import TourOrganizer

# Create your views here.


class TourOrganizerView(UserViewSet):
    serializer_class = UserSerializer
    organizer_serializer_class = TourOrganizerSerializer
    # permission_classes = []

    def get_organizer(self, request):
        user = request.user
        organizer = TourOrganizer.objects.get(user=user)
        serializer = self.organizer_serializer_class(organizer)
        return Response(serializer.data)

    def update_organizer(self, request):
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
