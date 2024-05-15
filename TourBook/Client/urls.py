from django.urls import path, include
from .views.CommentView import CommentView
from .views.ClientRequestView import ClientRequestView
app_name = "client"

client_requests_pattern = [
    path('create', ClientRequestView.as_view(
        {
            'post': 'create_request'
        }
    ))
]
client_comments_pattern = [
    path('', CommentView.as_view(
        {
            'get': 'get_tour_comments'
        }
    ))
]

urlpatterns = [
    path('<int:tour_id>/comments/', include(client_comments_pattern)),
    path('<int:tour_id>/tour-requests/', include(client_requests_pattern))
]
