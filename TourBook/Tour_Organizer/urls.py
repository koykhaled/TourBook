from django.urls import path, include
from .views.OrganizerView import TourOrganizerView
from .views.TourView import TourView, UnauthToursView, OrganizerTours, OtherOrganizersTours, TourRequests, TourPosted

from .views.TourPointView import TourPointView


app_name = 'tour_organizer'

organizer_patterns = [
    path(
        '<int:id>', TourOrganizerView.as_view(
            {
                'get': 'get_organizer',
                'patch': 'update_organizer',
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
    ),
    path('get-organizers', TourOrganizerView.as_view(
        {
            'get': 'get_organizers'
        }
    ))
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
    path('', TourRequests.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
]

tour_patterns = [
    path('', TourView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('unauth-tours', UnauthToursView.as_view({
        'get': 'get',
    })),
    path('organizer-tours', OrganizerTours.as_view({
        'get': 'list'
    })),
    path('<int:tour_id>/', TourView.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy',
    })),
    path('<int:tour_id>/post', TourPosted.as_view({
        'post': 'create',
    })),
    path('other-organizers-tours/', OtherOrganizersTours.as_view({
        'get': 'list'
    })),
    path('<int:tour_id>/tour-points/', include(tour_points_pattern)),
    path('<int:tour_id>/tour-requests/', include(tour_requests_pattern)),

]


urlpatterns = [
    path('', include(tour_patterns)),
    path('organizers/', include(organizer_patterns)),
]
