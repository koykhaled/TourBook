from django.urls import path, include
from .views.OrganizerView import TourOrganizerView
from .views.TourView import TourView
from .views.TourPointView import TourPointView


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
    ),
    path(
        'statistics', TourOrganizerView.as_view(
            {
                'get': 'get_organizer_statistics',
            }
        ),
        name='organizers-statistics'
    )
]

tour_points_pattern = [
    path('', TourPointView.as_view(
        {
            'get': 'get_tour_points',

        }
    )),
    path('<int:tour_point_id>', TourPointView.as_view(
        {
            # 'get': 'get_tour_point',
            'patch': 'update',
            'delete': 'delete',

        }
    ))
]

tour_requests_pattern = [
    path('', TourView.as_view(
        {
            'get': 'get_tour_requests',
            'post': 'handel_request'
        }
    )),
]

tour_patterns = [
    path('', TourView.as_view({
        'get': 'get_organizer_tours',
        'post': 'create',
    })),
    path('<int:tour_id>/', TourView.as_view({
        'get': 'get_tour',
        'post': 'post_tour',
        'patch': 'update_tour',
        'delete': 'delete',
    })),
    path('other-organizers-tours/', TourView.as_view({
        'get': 'get_other_organizers_tours'
    })),
    path('<int:tour_id>/tour-points/', include(tour_points_pattern)),
    path('<int:tour_id>/tour-requests/', include(tour_requests_pattern)),

]


urlpatterns = [
    path('', include(tour_patterns)),
    path('organizers/', include(organizer_patterns)),
]
