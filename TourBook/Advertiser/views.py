from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from .serializers.AdvertiserSerializers import AdvertiserSerializers
from accounts.serializers import UserSerializer

from Core.permissions import IsOrganizer

from .models.advertiser import Advertiser
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.



class AdvertiserView(APIView):
    serializer_class = AdvertiserSerializers

    def get(self, request):
        user = request.user
        try:
            advertiser = Advertiser.objects.get(user=user)
            serializer = self.serializer_class(advertiser)
            if all(value is not None for value in serializer.data.values()):
                data_status = 1

            return Response( serializer.data , 
                            status=status.HTTP_200_OK
                            )
        except Advertiser.DoesNotExist:
            return Response({"detail": "Advertiser not found."}, status=status.HTTP_404_NOT_FOUND)