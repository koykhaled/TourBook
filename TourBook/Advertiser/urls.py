from django.urls import path, include
from .views.AdvertiserView import AdvertiserView, AdvertisersView
from .views.OfferView import OfferView, OfferListAPIView, ActiveOffersAPIView
from .views.OfferRequestView import OfferRequestView


app_name = 'advertisers'

advertiser_patterns = [
    path('advertiser-detail/', AdvertiserView.as_view({
        'get': 'retrieve',
        'patch': 'update_advertiser'
    }), name="advertiser-detail"),
    path('', AdvertisersView.as_view(), name='advertisers')
]

offer_request_patterns = [
    path('', OfferRequestView.as_view({
        'get': 'get_offer_requests'
    })),
    path('<int:offer_request_id>/', OfferRequestView.as_view({
        'patch': 'handel_offer_requests'
    })),
]
offer_patterns = [
    path('', OfferListAPIView.as_view(), name='offers'),
    path('active-offers/', ActiveOffersAPIView.as_view(), name='offers'),
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
    )),
    path('<int:offer_id>/offer-requests/', include(offer_request_patterns))
]


urlpatterns = [
    path('', include(advertiser_patterns), name='advertiser'),
    path('offers/', include(offer_patterns), name='offers')
]
