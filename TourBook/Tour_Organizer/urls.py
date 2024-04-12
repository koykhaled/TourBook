from django.urls import path, include
from .views import TourOrganizerView

app_name = 'tour_organizer'

organizer_patterns = [
    path(
        '', TourOrganizerView.as_view(
            {
                'get': 'get_organizer',
                'post': 'update_organizer',
            }
        ),
        name='organizers'
    )
]

urlpatterns = [
    path('organizers/', include(organizer_patterns)),
]
