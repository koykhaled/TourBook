from django.urls import path, include
from .views import RegisterView


# app_name = 'accounts'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('register/',
         RegisterView.as_view({'post': 'register'}), name='register'),
    # path('update/', RegisterView.as_view({'patch': 'me'})),
]
