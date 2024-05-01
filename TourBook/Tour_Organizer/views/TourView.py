from rest_framework import viewsets, status
from rest_framework.response import Response

from Core.permissions import IsOrganizer
from ..serializers.TourSerializer import TourSerializer

from ..models.tour import Tour

from django.core import exceptions


class TourView(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    permission_classes = [IsOrganizer]

    def get_organizer_tours(self, request):
        try:
            tour_organizer = request.user.organizer
            tours = Tour.objects.filter(
                tour_organizer=tour_organizer).prefetch_related('tour_organizer')
            serializer = self.serializer_class(tours, many=True)
            return Response(
                {
                    'data': serializer.data,
                    'message': "retrive organizer tours done".title()
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_other_organizers_tours(self, request):
        try:
            tour_organizer = request.user.organizer
            tours = Tour.objects.exclude(
                tour_organizer=tour_organizer).prefetch_related('tour_organizer')
            serializer = self.serializer_class(tours, many=True)
            return Response(
                {
                    'data': serializer.data,
                    'message': "retrive other organizers tours done".title()
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_tour(self, request, tour_id):
        try:
            tour = Tour.objects.filter(
                pk=tour_id).prefetch_related('tour_organizer').get()
            serializer = self.serializer_class(tour)
            return Response(
                {
                    'data': serializer.data,
                    'message': "retrive tour done".title()
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        try:
            tour_organizer = request.user.organizer
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(tour_organizer=tour_organizer)
            return Response(
                {
                    'data': serializer.data,
                    'message': "Tour Created Successfully"
                },
                status=status.HTTP_201_CREATED
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception:
            return Response({
                'errors': serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, tour_id):
        try:
            tour = Tour.objects.get(pk=tour_id)
            serializer = self.serializer_class(
                tour, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': "Tour Updated Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception:
            return Response({
                'errors': serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )
