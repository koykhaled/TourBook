from django.apps import AppConfig


class TourOrganizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Tour_Organizer'

    def ready(self):
        try:
            import Tour_Organizer.signals
        except ImportError:
            pass
