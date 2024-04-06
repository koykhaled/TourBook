from django.urls import path, include
from .views import RegisterView
from djoser import views


# app_name = 'accounts'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('register/',
         RegisterView.as_view({'post': 'register'}), name='register'),
]
