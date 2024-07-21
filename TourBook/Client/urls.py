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

requests_pattern = [
    path('', ClientRequestView.as_view(
        {
            'get': 'get_client_requests',
            'post': 'create_request',
        }
    )),
    path('<int:request_id>/', ClientRequestView.as_view(
        {
            'delete': 'delete_request',
        }
    )),
]

client_requests_pattern = [
    path('', ClientRequestView.as_view(
        {
            'get': 'get_client_requests',
        }
    )),
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
    path('<int:tour_id>/requests/', include(requests_pattern)),
    path('client-requests/', include(client_requests_pattern)),
]
