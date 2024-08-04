from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.AdvertiserSerializers import AdvertiserSerializers
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from Core.permissions.AdvertiserPermissions import IsAdvertiserOwnerProfile

from ..models.advertiser import Advertiser
from django.core import exceptions

from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve Advertiser Profile", tags=["Advertiser Profile"]),
    update_advertiser=extend_schema(summary="Update Advertiser Profile",
                                    tags=["Advertiser Profile"]),
)
class AdvertiserView(UserViewSet):
    serializer_class = UserSerializer
    advertiser_serializer_class = AdvertiserSerializers
    permission_classes = [IsAdvertiserOwnerProfile]

    def retrieve(self, request, advertiser_id):
        """
        Retrieve the advertiser data by id.

        This method returns the serialized data of the Touradvertiser instance associated with the authenticated user.
        It checks if all fields in the serialized data have a value (not None) and sets the data_status accordingly.

        Returns:
            Response: Serialized data of the advertiser and status indicating the data_status.
        """
        try:
            advertiser = Advertiser.objects.get(pk=advertiser_id)
            serializer = self.advertiser_serializer_class(advertiser)

            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Advertiser does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False)
    def update_advertiser(self, request, advertiser_id):
        """
        Update the advertiser data by id.

        This method allows updating the user and advertiser data associated with the authenticated user.
        It performs partial updates on the user and advertiser instances based on the provided request data.

        Args:
            id (int) : id of the advertiser
            request (Request): The HTTP request containing the updated user and advertiser data.
            request contain to dictionaries :
                user => contain user data [phone , email , username] for updating and send email when user change his email
                advertiser => contain advertiser data [address , evaluation , situation , logo]

        Returns:
            Response: Serialized data of the updated advertiser or error response if validation or update fails.
        """
        try:
            user = request.user
            advertiser = Advertiser.objects.get(pk=advertiser_id)
            user_serializer = self.serializer_class(user)
            advertiser_serializer = self.advertiser_serializer_class(
                advertiser)
            errors = []

            # don't forget to apply SRP
            if 'user' in request.data and request.data['user']:
                user_serializer = self.serializer_class(
                    user, data=request.data['user'], partial=True)
                if not user_serializer.is_valid(raise_exception=False):
                    errors.append(user_serializer.errors)
                else:
                    self.perform_update(user_serializer)

            if 'advertiser' in request.data:
                advertiser_serializer = self.advertiser_serializer_class(
                    advertiser, data=request.data['advertiser'], partial=True)
                if not advertiser_serializer.is_valid(raise_exception=False):
                    errors.append(advertiser_serializer.errors)
                else:
                    advertiser_serializer.save()

            if errors:
                raise exceptions.ValidationError(errors)

            return Response(
                {
                    'data': advertiser_serializer.data,
                    'message': 'advertiser Updated Successfully'
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ValidationError as e:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        summary="Get Advertisers List", tags=["Advertisers"]),
)
class AdvertisersView(APIView):
    serializer_class = AdvertiserSerializers

    @action(detail=False)
    def get(self, request):
        try:
            advertisers = Advertiser.objects.all()
            serializer = self.serializer_class(advertisers, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Advertiser.DoesNotExist:
            return Response({"detail": "Advertiser not found."}, status=status.HTTP_404_NOT_FOUND)
