from django.apps import AppConfig


class AdvertiserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Advertiser'

    def ready(self):
        try:
            import Advertiser.signals
        except ImportError:
            pass
