from rest_framework import status, viewsets
from rest_framework.response import Response
from Core.permissions.OrganizerPermissions import IsTourOwnerOrReadOnly
from ..serializers.TourPointSerializer import TourPointSerializer
from ..models.tour import Tour
from django.core import exceptions
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(

    list=extend_schema(summary="List all tour points", tags=["Tour Points"]),
    update=extend_schema(summary="Update a tour point", tags=["Tour Points"]),
    destroy=extend_schema(summary="Delete a tour point", tags=["Tour Points"]),
)
class TourPointView(viewsets.ModelViewSet):
    serializer_class = TourPointSerializer
    permission_classes = [IsTourOwnerOrReadOnly]

    def list(self, request, tour_id):
        try:
            tour = Tour.objects.prefetch_related('tour_points').get(pk=tour_id)
            tour_points = tour.tour_points.all()
            serializer = self.serializer_class(tour_points, many=True)
            return Response(
                {
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError:
            return Response({
                'errors': serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, tour_id, tour_point_id):
        try:
            tour = Tour.objects.prefetch_related('tour_points').get(pk=tour_id)
            tour_point = tour.tour_points.get(pk=tour_point_id)
            serializer = self.serializer_class(
                tour_point, data=request.data, partial=True)
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': "Tour Point Updated Successfully"
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
                'errors': serializer.errors
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, tour_id, tour_point_id):
        try:
            tour = Tour.objects.prefetch_related('tour_points').get(pk=tour_id)
            tour_point = tour.tour_points.get(pk=tour_point_id)
            tour_point.delete()
            return Response(
                {
                    'message': "Tour Point Deleted Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
