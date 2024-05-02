from django.urls import path, include
from .views.OrganizerView import TourOrganizerView
from .views.TourView import TourView

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

tour_patterns = [
    path('', TourView.as_view({
        'get': 'get_organizer_tours',
        'post': 'create',
    })),
    path('<int:tour_id>/', TourView.as_view({
        'get': 'get_tour',
        'patch': 'update',
        'delete': 'delete',
    })),
    path('other-organizers-tours/', TourView.as_view({
        'get': 'get_other_organizers_tours'
    })),

]

urlpatterns = [
    path('', include(tour_patterns)),
    path('organizers/', include(organizer_patterns)),
]
