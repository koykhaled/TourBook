from django.urls import path, include
# from .views import AdvertisersView, OfferListAPIView, ActiveOffersAPIView
from .views.AdvertiserView import AdvertiserView


app_name = 'advertisers'

advertiser_patterns = [
    path('<int:advertiser_id>/', AdvertiserView.as_view({
        'get': 'retrieve',
        'patch': 'update_advertiser'
    }))
]

urlpatterns = [
    path('advertisers/', include(advertiser_patterns), name='advertiser'),
    # path('offers/', OfferListAPIView.as_view(), name='offers'),
    # path('active_offers/', ActiveOffersAPIView.as_view(), name='offers'),
    # path('advertisers/<int:user>/',
    #      AdvertiserView.as_view(), name='advertiser-detail'),
]
