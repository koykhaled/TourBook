from django.urls import path, include
from .views.CommentView import CommentView

app_name = "client"

urlpatterns = [
    path('<int:tour_id>/comments', CommentView.as_view(
        {
            'get': 'get_tour_comments'
        }
    ))
]
