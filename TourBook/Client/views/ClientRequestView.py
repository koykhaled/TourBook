from rest_framework import status, viewsets
from rest_framework.response import Response
from ..serializers.ClientRequestserializer import ClientRequestSerializer
from Core.permissions import IsClient
from Tour_Organizer.models.tour import Tour
from ..models.client import Client
from django.core import exceptions
from django.db import IntegrityError


class ClientRequestView(viewsets.ModelViewSet):
    serializer_class = ClientRequestSerializer
    permission_classes = [IsClient]

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
