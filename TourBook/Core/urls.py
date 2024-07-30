from django.urls import path, include
from .views.ReportView import ReportView
from .views.NotificationView import NotificationView


app_name = 'core'

report_patterns = [
    path('<int:organizer_id>', ReportView.as_view({
        'post': "create_report"
    }))
]

notification_patterns = [
    path('', NotificationView.as_view({
        'get': 'get_notifications'
    }))
]

urlpatterns = [
    path('reports/', include(report_patterns)),
    path('notifications/', include(notification_patterns)),
]
