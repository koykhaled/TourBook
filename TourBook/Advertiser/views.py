from rest_framework.response import Response
from rest_framework import status , generics
from django.core.exceptions import ValidationError

from Core.models.user import UserAccount
from Advertiser.models.offers import Offer
from .serializers.OfferSerializer import ActiveOffersSerializer

from .serializers.AdvertiserSerializers import AdvertiserSerializers , OfferSerializer
from accounts.serializers import User, UserSerializer
from django.db.models import Q
from Core.permissions import IsOrganizer
from datetime import datetime, timedelta
from .models.advertiser import Advertiser
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.



class AdvertiserView(APIView):
    serializer_class = AdvertiserSerializers

    def get(self, request):        
        try:
            advertisers = Advertiser.objects.all()
            serializer = self.serializer_class(advertisers, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Advertiser.DoesNotExist:
            return Response({"detail": "Advertiser not found."}, status=status.HTTP_404_NOT_FOUND)



class SingleAdvertiserAPIView(APIView):
    serializer_class = AdvertiserSerializers
    queryset = Advertiser.objects.all()
    lookup_field = 'user'

    def get(self, request, user):
        try:
            advertiser = Advertiser.objects.select_related('user').prefetch_related('offers').get(user=user)
            serializer = AdvertiserSerializers(advertiser)
            return Response(serializer.data)
        except Advertiser.DoesNotExist:
            return Response({'error': 'Advertiser not found'}, status=404)

class OfferListAPIView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer



# class ActiveOffersAPIView(APIView):
#     def get(self, request):
#         current_date = datetime.now()
#         active_offers = Offer.objects.filter(end_date__gt=current_date)
#         serializer = ActiveOffersSerializer(active_offers, many=True)
#         return Response(serializer.data)
class ActiveOffersAPIView(APIView):
    def get(self, request):
        current_date = datetime.now()
        query = Q(end_date__gt=current_date)

        day = request.GET.get('day')
        if day:
            # Filter by day (end_date__date > given day)
            query &= Q(end_date__date__gt=day)

        service = request.GET.get('service')
        if service:
            # Filter by service
            query &= Q(service__service_field=service)

        title = request.GET.get('title')
        if title:
            # Filter by title
            query &= Q(title__icontains=title)

        active_offers = Offer.objects.filter(query)
        serializer = ActiveOffersSerializer(active_offers, many=True)
        return Response(serializer.data)