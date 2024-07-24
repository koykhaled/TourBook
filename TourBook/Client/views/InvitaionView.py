from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from Core.permissions.ClientPermissions import IsClientOwnerProfile
from django.core import exceptions
from ..serializers.InvetationSerializer import InvetationSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    send_invetation=extend_schema(
        summary="Invite Freinds for a Tour", tags=['Tour Invetation']
    )
)
class InvetationView(viewsets.ModelViewSet):
    permission_classes = [IsClientOwnerProfile]
    serializer_class = InvetationSerializer

    @action(detail=False)
    def send_invetation(self, request, tour_id):
        try:
            serializer = self.serializer_class(
                data=request.data, context={'request': request, 'tour_id': tour_id})

            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            serializer.save()
            return Response({"message": "Your Invetation Sent Successfully!!"}, status=status.HTTP_201_CREATED)

        except exceptions.ValidationError:
            return Response({
                'errors': serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour dose not exist!!"
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
