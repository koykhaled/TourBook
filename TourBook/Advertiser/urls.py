from django.urls import path, include
# from .views import AdvertisersView, OfferListAPIView, ActiveOffersAPIView
from .views.AdvertiserView import AdvertiserView
from .views.OfferView import OfferView


app_name = 'advertisers'

advertiser_patterns = [
    path('<int:advertiser_id>/', AdvertiserView.as_view({
        'get': 'retrieve',
        'patch': 'update_advertiser'
    }))
]

offer_patterns = [
    path('advertiser-offers', OfferView.as_view(
        {
            "get": "get_advertiser_offers",
            'post': "create_offer"
        }
    )),
    path('', OfferView.as_view(
        {
            'post': "create_offer"
        }
    )),
    path('<int:offer_id>', OfferView.as_view(
        {
            'get': "get_offer",
            'patch': "update_offer",
        }
    ))
]

urlpatterns = [
    path('advertisers/', include(advertiser_patterns), name='advertiser'),
    path('offers/', include(offer_patterns), name='offers')
    # path('offers/', OfferListAPIView.as_view(), name='offers'),
    # path('active_offers/', ActiveOffersAPIView.as_view(), name='offers'),
    # path('advertisers/<int:user>/',
    #      AdvertiserView.as_view(), name='advertiser-detail'),
]
