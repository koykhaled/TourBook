from django.urls import path, include
from .views import AdvertiserView


app_name = 'advertisers'

urlpatterns = [
    path('advertiser', AdvertiserView.as_view(), name='advertiser'),
]