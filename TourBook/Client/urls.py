from django.urls import path, include
from .views.CommentView import CommentView
from .views.ClientRequestView import ClientRequestView
from .views.ClientView import ClientView
app_name = "client"


client_patterns = [
    path('<int:client_id>/', ClientView.as_view(
        {
            'get': 'retrieve',
            'patch': 'update_client',
        }
    ))
]

client_requests_pattern = [
    path('create', ClientRequestView.as_view(
        {
            'post': 'create_request'
        }
    ))
]
comments_pattern = [
    path('', CommentView.as_view(
        {
            'get': 'get_tour_comments',
            'post': 'create_comment',
        }
    )),
    path('<int:comment_id>/', CommentView.as_view(
        {
            'delete': 'delete_comment',
            'patch': 'update_comment',
        }
    ))
]


urlpatterns = [
    path('clients/', include(client_patterns)),
    path('<int:tour_id>/comments/', include(comments_pattern)),
    path('<int:tour_id>/tour-requests/', include(client_requests_pattern))
]
