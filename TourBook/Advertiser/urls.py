from django.urls import path, include
from .views import AdvertiserView ,SingleAdvertiserAPIView,OfferListAPIView,ActiveOffersAPIView


app_name = 'advertisers'

urlpatterns = [
    path('advertisers/', AdvertiserView.as_view(), name='advertiser'),
    path('offers/', OfferListAPIView.as_view(), name='offers'),
    path('active_offers/', ActiveOffersAPIView.as_view(), name='offers'),
    path('advertisers/<int:user>/', SingleAdvertiserAPIView.as_view(), name='advertiser-detail'),
]