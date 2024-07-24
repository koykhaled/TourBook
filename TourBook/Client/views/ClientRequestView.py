from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers.ClientRequestserializer import ClientRequestSerializer
from Core.permissions.ClientPermissions import IsRequestOwnerOrReadOnly
from Tour_Organizer.models.tour import Tour
from ..models.client import Client
from django.core import exceptions
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get_client_requests=extend_schema(
        summary="get Client Requests", tags=['Client Request']),
    create_request=extend_schema(
        summary="create a request for the tour", tags=['Client Request']),
    delete_request=extend_schema(
        summary="Cancel a request", tags=['Client Request']),
)
class ClientRequestView(viewsets.ModelViewSet):
    serializer_class = ClientRequestSerializer
    permission_classes = [IsRequestOwnerOrReadOnly]

    @action(detail=False)
    def get_client_requests(self, request):
        try:
            client = request.user.client
            requests = client.client_requests.all()
            serializer = self.serializer_class(requests, many=True)
            return Response({
                "data": serializer.data
            })
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Client Dosen't Exist!!"
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: ClientRequestSerializer,
            status.HTTP_400_BAD_REQUEST: 'Error message',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Error message'
        }
    )
    @action(detail=False)
    def create_request(self, request, tour_id):
        try:
            client = Client.objects.get(user=request.user)
            tour = Tour.objects.prefetch_related('tour_points').get(pk=tour_id)
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            serializer.save(tour_object=tour, client_object=client)
            return Response(
                {
                    'data': serializer.data,
                    'message': "Request Created Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except exceptions.ValidationError as e:
            return Response({
                'errors': serializer.errors or e
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        request={'request_id': "int"},
        responses={
            status.HTTP_200_OK: "Request Deleted Successfullt",
            status.HTTP_400_BAD_REQUEST: 'Error message',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Error message'
        }
    )
    @action(detail=False)
    def delete_request(self, request, tour_id, request_id):
        try:
            tour = Tour.objects.prefetch_related(
                'tour_requests').get(pk=tour_id)
            request = tour.tour_requests.get(pk=request_id)
            request.delete()
            return Response(
                {
                    'message': "Request Deleted Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
