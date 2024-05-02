from django.apps import AppConfig


class TourOrganizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Tour_Organizer'

    def ready(self):
        import Tour_Organizer.signals
