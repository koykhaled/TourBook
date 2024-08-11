from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ..serializers.ServiceSerializer import ServiceSerializer
from ..models.service import Service

from Core.permissions.AdvertiserPermissions import IsAdvertiserOwnerProfile

from drf_spectacular.utils import extend_schema, extend_schema_view

from ..models.advertiser import Advertiser

from django.core import exceptions
from datetime import datetime
from django.db.models import Q

from rest_framework.views import APIView


@extend_schema_view(
    get_services=extend_schema(
        summary="Get Services", description="you need JWT Token to show the offers", tags=['Services']),
    create_servcie=extend_schema(
        summary="create a Service", tags=['Services']),
)
class ServiceView(viewsets.ModelViewSet):

    serializer_class = ServiceSerializer
    permission_classes = [IsAdvertiserOwnerProfile]

    @action(detail=False)
    def get_services(self, request):
        try:
            services = Service.objects.all()

            serializer = self.serializer_class(services, many=True)
            return Response(
                {
                    'data': serializer.data,
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False)
    def create_service(self, request):
        # don't forget to apply image classification
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    'data': serializer.data,
                    'message': "Service Created Successfully"
                },
                status=status.HTTP_201_CREATED
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except (exceptions.ValidationError, TypeError) as e:
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
